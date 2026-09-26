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

No length target: the length follows the argument (about 150 words per minute).

### 1. Two runs

> Here's a small Python project with one failing test. We set up an LLM agent, a program that lets a model work on a task step by step, and asked it to fix the test, twice.
> Same model, same files, same task. And both runs began the same way. They listed the files, read the test, read the code, and fixed the same bug.
> Then they split. Run A took four more steps. Its last reply began "Fixed", and ended "All tests now pass."
> Run B stopped right there. Its reply also began "Fixed", and said its code now matched the values the test expects.
> So we ran the test ourselves. After run A, it passes. After run B, it still fails.
> That wasn't luck. We ran each version three times. Every run like A passed. Every run like B said "Fixed", and failed.
> Run B was missing one thing: a way to run the test. The model was the same. So what is an LLM agent, that taking away one tool leaves it sure of something false?

*Screen:* the project at top right as three file cards, report.py, test_report.py and sales.csv, with a red cross on test_report.py (the test fails). Two strips of cards along the bottom half, labelled "run A" and "run B", built card by card in step with the narration from the real runs (captures/loop_1.json, captures/no_tests_1.json): a grey card, then a white card (the task), then pairs of cards, a blue card naming the tool the model asked for ("list", "read test_report.py", "read report.py", "write report.py") and a green card for what came back. The four pairs appear in both strips at once. Then run A's strip grows four more pairs ("run tests", with a small red cross on its green card; "read sales.csv"; "write report.py"; "run tests", with a small check on its green card) and ends in a blue card "Fixed."; run B's ends in a blue card "Fixed." right after its fourth pair. Beside each final card, the real reply, abridged: A: "Fixed. The test was failing for two reasons … All tests now pass."; B: "Fixed. … now returns the correct totals per region, matching the expected values in test_report.py." Then our own test run after each (captures, "test_after"): A: a check and "OK"; B: a red cross and "KeyError: 'region'". Then "3 of 3" beside each (data/runs.txt). No explanation of the colours yet. The strips stay on screen.

### 2. A model on its own

> To see what's going on, build it up from the start: a model on its own.
> An LLM reads text and writes text. You send it some, and it writes what comes next.
> Everything it reads on one call is called its context. Here, that's some instructions and our task.
> It replies with text, of course. It even writes out a shell command it would like to run.
> But nothing runs text. The command never ran, the model never saw a single file, and the test still fails.
> For anything to change, something else has to act on what the model writes.

*Screen:* the strips from chapter 1 slide down and fade to a faint outline, keeping their place. A box labelled "model" appears top centre, with a small tag under it: "claude -p, tools off". Along the bottom, a new strip starts: a grey card "instructions" and a white card "task". The model box reads the strip: a light band sweeps it from left to right. Then a blue card drops from the model onto the end of the strip, and opens into the real reply (captures/bare_1.json): "I'll look at the test and the report.py file to understand what's failing." then "Tool: bash" and `{"command":"find /home/user/space-invaders -maxdepth 3 -iname '*report*' …}`, the command in a mono box. A dashed line from the command toward the project cards stops short; the project doesn't change, and the red cross on test_report.py stays.

### 3. One tool call

> So let's act for it. We add a list of tools to the instructions: list the files, read a file, write a file, and run the tests. Each is ordinary code, written by us.
> We also tell the model how to ask for one: reply with one line of JSON that names the tool. That message is called a tool call.
> Now the model's first reply is a tool call: list the files.
> Our code reads the tool call, runs the tool, and adds its output to the context. That's the tool result.
> Notice who ran it. Not the model. It only asked. Anthropic's documentation puts it plainly: the model never executes anything on its own.
> Then we call the model again, and it asks for a second tool: read the test. But our code stops here. It was written for one tool call.
> The model can't know in advance how many steps it will need. So our code shouldn't decide that either.

*Screen:* the bare strip clears back to its grey card, which widens as four tool names appear on it one by one (list_files, read_file, write_file, run_tests); the format line appears in the grey card, as the system prompt gives it: `{"tool": "read_file", "path": "report.py"}`. A box labelled "our code" appears between the model and the project. The real run (captures/one_tool_1.json): the band sweeps the strip; a blue card `{"tool": "list_files"}` drops onto the strip, and an arrow carries it to "our code", which touches the project; a green card comes back and joins the strip, opening briefly to show "report.py sales.csv test_report.py". The band sweeps again, and a blue card `{"tool": "read_file", "path": "test_report.py"}` drops onto the strip; "our code" stays still; the card's outline pulses, unanswered.

### 4. The loop

> Therefore, a loop. Call the model. If its reply is a tool call, run the tool, and add the result to the context. Then call the model again.
> Stop when it replies without a tool call, or after twenty calls, in case it never does.
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

*Screen:* the run_tests card goes to "our code", the project's test runs, and a green card with a red cross joins the strip; it opens on the real output's last lines (captures/loop_1.json): `KeyError: 'region'` and `FAILED (errors=1)`. The band sweeps; the blue card `{"tool": "read_file", "path": "sales.csv"}`; the green card opens on the file's first line, `region,product,units,unit_price`, with a small red marker drawn just before "region" (the byte order mark, U+FEFF, which prints as nothing), labelled "byte order mark". Then write_file report.py (opening on `open(path, newline="", encoding="utf-8-sig")`, the encoding highlighted), run_tests (green card with a check, "OK"), and the final blue card "Fixed." The red cross on test_report.py turns into a check. Then above the strip, the scripted path as three grey chips, "read", "fix", "test", ending in a red cross, tagged "scripted (not run)", and under it the real path as the blue cards' names, the chips after the first test run highlighted.

### 6. What the model remembers

> Run A called the model nine times: eight tool calls, then the final reply.
> It looks as if the model worked through the problem, remembering what it had tried. It didn't. Each of those calls started from nothing.
> The model keeps nothing between calls. So our loop sends it the whole context every time: the instructions, the task, and every tool call and result so far.
> Here's how much it read on each call, counted in tokens, the chunks of text a model reads. The first call read about fourteen hundred.
> Most of that is fixed text: our instructions, and notes that the command-line tool we call the model through adds to every call.
> The ninth read about twenty-seven hundred: everything the first call read, and everything since.
> Together, the nine calls read about eighteen and a half thousand tokens, to change two lines of code.
> This isn't a quirk of our code. Anthropic's documentation says the same of its Messages API: it's stateless, so you always send the full conversation.
> The model still knows what it learned in training. That's how it knew what a byte order mark was.
> But what it has tried in this task, and what came back, it knows only from its context. The context is its only memory of the task.

*Screen:* the strip's cards keep their order and colours but change width to the number of tokens each adds (captures/loop_1.json: each call's context minus the one before; within a call's addition, split between the model's card and the tool result's card by characters), so the grey instructions block, most of the first call, becomes the widest; it splits into two shades, a wide one labelled "notes added by claude -p ≈1,180" and a narrow one "our instructions + task ≈240" (data/overhead.txt). Then the strip is copied upward once per call, each copy cut at that call's length, making a staircase of nine rows: row n is what call n read. Beside each row, its count in amber: 1,423 for the first, 2,745 for the ninth, the others smaller and fainter. A band sweeps each row from the left as its count appears. Then an amber total under the staircase: 18,537 tokens read. The green card with the red cross (the KeyError) is outlined in every row from the sixth call on.

### 7. Run B

> Now run B makes sense. It's the same loop and the same model. The only difference is the tool list: there's no run tests.
> Its first four steps match run A's. Then, where run A asked to run the test, run B had nothing to ask for.
> So it replied. Look at its context when it did: its own fix, and nothing after it. No tool result could have told it the fix was incomplete.
> It looks as if the model knew it had succeeded. It didn't. It only knew that nothing in its context said otherwise.
> Its "Fixed" wasn't a lie. It was a reasonable conclusion, from a context with no evidence against it.
> It could have read the data file. It had the tool. It just didn't see a reason to.
> Would a more capable model do better? We ran run B three more times, with one.
> Twice, with no way to run the test, it read the data file to check the sums by hand. It found the mark, and fixed both bugs. And it said plainly that it couldn't run the test.
> It did better the same way run A did: it put more ground truth into its own context.
> The third time, it asked for the data file in a format our code didn't recognise. Our loop saw no tool call, and stopped.
> So this is why agents work, and the first way they break down. Each step can put ground truth into the context. Where nothing checks the work, the model's own guess has the last word.
> If that guess were one step in a longer task, the next call would read it as fact and build on it. Nothing here would catch that either. It's called compounding errors.

*Screen:* the staircase folds back into run A's single strip of cards, which moves up; run B's strip is built beneath it card by card, cards aligned (captures/no_tests_1.json). B's grey card shows its tool list with run_tests missing. B's first four pairs line up under A's. At the fifth position, A's `run_tests` card and its green card with the red cross are outlined; under them, B's final blue card, "Fixed.", and then empty space where A's strip goes on. B's reply opens in full above its card (the real text, as in chapter 1). Then B's final card and the empty space are bracketed, the empty space labelled "no test result". For the more capable model (captures/no_tests_strong_1.json to _3.json), three short strips appear under B's, labelled "more capable model": two whose blue cards include "read sales.csv", each followed by a green card with the red byte-order-mark marker, ending in "Fixed" and a check (our test run: OK), with the real reply's first line beside the first, "I fixed report.py, but I couldn't run the test because I have no tool to execute code. I checked the result by hand against sales.csv instead."; and one that ends after "read report.py" in a blue card showing its real reply, `<invoke_read_file> <parameter name="path">sales.csv</parameter> </invoke_read_file>`, with "our code: no tool call found, loop stops" and a red cross (our test run: FAIL). Then the label "nothing checks the work" at the top left. For the last line, B's "Fixed." card is outlined in red and the label "compounding errors" appears under the first.

### 8. The context grows

> The second way agents break down is in the staircase: the context only grows. Every step adds to it, and every call reads all of it.
> Here's the same task, run once by Claude Code, Anthropic's coding agent. It's the same command-line tool we've been calling the model through, now running its own loop, with its tools narrowed to match ours: read, edit, and run the test.
> Its first call read about eleven thousand six hundred tokens: its instructions, its tool descriptions, and our task.
> It found both bugs in nine calls, like run A. But it read those instructions again on every call, so in all it read over a hundred and twenty thousand tokens.
> And a longer task costs more than its length suggests. Each new call re-reads everything before it, so twice the calls means more than twice the reading.
> Reading more isn't only slower and costlier. As a context grows, models get worse at recalling what's in it. Researchers call this context rot. Our runs are far too short to show it.

*Screen:* the label "the context grows" at the top left. Run A's staircase from chapter 6, then its strip in token widths, at the chapter 6 scale; then Claude Code's first-call context (captures/claude_code_1.parsed.json) drawn at the same scale as a grey block that runs off the right edge; the view zooms out until it fits, and run A's whole strip becomes a short bar beside it. Its per-call counts as a staircase of nine rows (11,597 to 15,620, in amber; "9 calls"), the grey part of every row outlined, and the amber total, 123,192. For "twice the calls", run A's staircase with a second copy of its rows stacked on top, each longer, and the area beside it. Then the label "context rot · Hong, Troynikov and Huber (Chroma), 2025".

### 9. The answer

> So why did one missing tool leave run B sure of something false? Because an agent is a model that picks each next step from its context, not from a script.
> And a loop that runs those steps, and writes the results back in. About the task, the model remembers nothing else.
> Run A's context held ground truth from the test. Run B's held only its own fix. Same model, different context.
> The more capable model did better in just that way: it read the data for itself. And it said what it hadn't been able to check.
> That's also why coding suits agents so well, as Anthropic's guide points out. Code comes with tests: an answer the agent can check its work against at every step.
> We've skipped a lot here: planning, memory that lasts between tasks, and teams of agents. But each of those still reaches the model the same way: through its context.
> So when you build an agent, or hand one a task, don't only ask how clever the model is. Ask what will tell it that it's wrong.

*Screen:* the two strips from chapter 1, as cards, now with their colours named once, small: grey "instructions", blue "the model's replies", green "tool results". A's green card with the red cross is outlined; the matching place in B's strip is empty. Then the loop picture from chapter 4 (model, our code, project, strip) settles in the middle. End card: the takeaway, and references: Anthropic, "Building effective agents" (Schluntz and Zhang, 2024); Anthropic, "Effective context engineering for AI agents" (2025); Claude API documentation, "How tool use works" and "Using the Messages API"; Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (2022); Willison, "I think 'agent' may finally have a widely enough agreed upon definition to be useful jargon now" (2025); Hong, Troynikov and Huber, "Context Rot: How Increasing Input Tokens Impacts LLM Performance" (Chroma, 2025).

