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

> Here's a small Python project with one failing test. We asked an LLM to fix it, twice, in two separate runs.
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

*Screen:* the strips from chapter 1 slide down and fade to a faint outline, keeping their place. A box labelled "model" appears top centre. Along the bottom, a new strip starts: a grey card "instructions" and a white card "request". The model box reads the strip: a light band sweeps it from left to right. Then a blue card drops from the model onto the end of the strip, and opens into the real reply (captures/bare_1.json): "I'll look at the test and the report.py file to understand what's failing." then "Tool: bash" and `{"command":"find /home/user/space-invaders -maxdepth 3 -iname '*report*' …}`, the command in a mono box. A dashed line from the command toward the project cards stops short; the project doesn't change, and the red cross on test_report.py stays.

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

> Therefore, a loop. Call the model. If its reply is a tool call, run the tool, add the result to the context, and call the model again. Stop when it replies without one.
> That loop, with a model and some tools, is the whole agent. One common definition says just that: an LLM agent runs tools in a loop to achieve a goal.
> Here's run A, step by step. It lists the files, reads the test, and reads the code. And it spots the bug: the code adds the units to the price, where it should multiply them.
> It rewrites that line, then asks to run the test.
> Pause here, and make a prediction. The model found a real bug, and fixed it. Will the test pass?

*Screen:* "our code" turns into a loop: an arrow from the model's card down to "our code", on to the project, back into the strip, and up to the model. Beside it, the code card, exactly as in sims/agent.py (`def agent(task, tools, max_calls=20):` and its body: build the context from the task; for each call, call the model with the context, append its reply, parse a tool call; if there is none, return; otherwise run the tool and append its result), with a small note under it: "the model's tool call is a line of JSON; APIs give it a structured form". Then the replay of run A (captures/loop_1.json) on the strip, one call per pair of cards, the band sweeping before each blue card: list_files, read_file test_report.py, read_file report.py (its green card opens on the line `... + int(row["units"]) + float(row["unit_price"])`, the second plus highlighted), write_file report.py (the card opens on the same line with `*`). Then a blue card `{"tool": "run_tests"}` drops onto the strip, and everything stops: the arrow to "our code" waits. The pause holds for about three seconds.

### 5. The test answers

> It doesn't. The test fails with a key error: there's no column called "region".
> That result goes into the context, like any other. And on the next call, the model reads it, and changes course: it asks to see the data file.
> The file begins with an invisible character, called a byte order mark, glued to the front of the word "region". The code was only half the problem.
> The model changes how the file is opened, so the mark is skipped. It runs the test again, and this time it passes. Then it replies with no tool call, and the loop ends.
> Notice who decided to look at the data file. Not our code: it only ran what was asked.
> If our code had fixed the steps in advance, say read, fix, and test, that would be called a workflow. And that workflow would have ended at the key error.
> In an agent, the model picks each next step from what's in its context. Here, that included the test's answer.

*Screen:* the run_tests card goes to "our code", the project's test runs, and a green card with a red cross joins the strip; it opens on the real output's last lines (captures/loop_1.json): `KeyError: 'region'` and `FAILED (errors=1)`. The band sweeps; the blue card `{"tool": "read_file", "path": "sales.csv"}`; the green card opens on the file's first line, `region,product,units,unit_price`, with a small red marker drawn just before "region" (the byte order mark, U+FEFF, which prints as nothing), labelled "byte order mark". Then write_file report.py (opening on `open(path, newline="", encoding="utf-8-sig")`, the encoding highlighted), run_tests (green card with a check, "OK"), and the final blue card "Fixed." The red cross on test_report.py turns into a check. Then above the strip, the scripted path as three grey chips, "read", "fix", "test", ending in a red cross, and under it the real path as the blue cards' names, the chips after the first test run highlighted.

### 6. What the model remembers

> It looks as if the model worked through the problem, remembering what it had tried. It didn't. Each of those nine calls started from nothing.
> The model keeps nothing between calls. So our loop sends it the whole context every time: the instructions, the request, and every tool call and result so far.
> Here's how much it read on each call, counted in tokens, the word pieces a model reads. The first call read about fourteen hundred.
> The ninth read about twenty-seven hundred: everything the first call read, and everything since.
> Across the nine calls, that's about eighteen and a half thousand tokens, to change two lines of code.
> This isn't a quirk of our code. Anthropic's API documentation says the API is stateless: you always send the full conversation.
> So the context is the model's only memory. Whatever isn't in it, the model doesn't know.

*Screen:* the strip's cards keep their order and colours but change width to the number of tokens each adds (captures/loop_1.json: each call's context minus the one before; within a call's addition, split between the model's card and the tool result's card by characters), so the grey instructions block, most of the first call, becomes the widest. Then the strip is copied upward once per call, each copy cut at that call's length, making a staircase of nine rows: row n is what call n read. Beside each row, its count in amber: 1,423 for the first, 2,745 for the ninth, the others smaller and fainter. A band sweeps each row from the left as its count appears. Then an amber total under the staircase: 18,537 tokens read. The green card with the red cross (the KeyError) is outlined in every row from the sixth call on.

### 7. Run B

> Now run B makes sense. It's the same loop and the same model. The only difference is the tool list: there's no run tests.
> Its first four steps match run A's. Then, where run A asked to run the test, run B had nothing to ask for.
> So it replied. Look at its context when it did: its own fix, and nothing after it. No tool result could have told it the fix was incomplete.
> Its "Fixed" wasn't a lie. It was a reasonable conclusion, from a context with no evidence against it.
> It could have read the data file. It had the tool. But nothing in its context gave it a reason to.

*Screen:* the staircase folds back into run A's single strip of cards, which moves up; run B's strip is built beneath it card by card, cards aligned (captures/no_tests_1.json). B's grey card shows its tool list with run_tests missing. B's first four pairs line up under A's. At the fifth position, A's `run_tests` card and its green card with the red cross are outlined; under them, B's final blue card, "Fixed.", and then empty space where A's strip goes on. B's reply opens in full above its card (the real text, as in chapter 1). Then B's final card and the empty space are bracketed.

### 8. Where it breaks

> That's why agents work: each step can put the world's answer into the context. It also shows where they break.
> The first way is the one we just saw. Where nothing checks the work, the model's own guess has the last word.
> The second is that the context only grows. Every step adds to it, and every call reads all of it.
> Here's the same task, run once by Claude Code, a production agent. Its first call read about eleven and a half thousand tokens: its instructions, its tool descriptions, and our one request.
> It found both bugs in nine calls, and read over a hundred and twenty thousand tokens along the way.
> Longer tasks take many more steps, so the total read grows faster than the number of steps. And the longer the context, the worse a model gets at recalling what's in it. Anthropic's engineers call this context rot.
> The third: whatever lands in the context stays there, and is read again on every call. Here that was the test's answer, and it helped. A wrong result, or a wrong guess, would be read again just the same, and every later step would build on it.

*Screen:* three short labels appear one at a time at the top left as each way is named: "nothing checks the work", "the context grows", "errors stay". For the first, B's strip with its bracket, small. For the second, run A's strip in token widths, at the chapter 6 scale; then Claude Code's first-call context (captures/claude_code_1.parsed.json) drawn at the same scale as a grey block that runs off the right edge; the view zooms out until it fits, and run A's whole strip becomes a short bar beside it. Its per-call counts as a staircase of nine rows (11,597 to 15,620, in amber) and the amber total, 123,192. Then the label "context rot · Anthropic, 2025". For the third, run A's staircase from chapter 6 again, with the KeyError card outlined in every row after it arrives; then the outline turns from green to red on every row at once, to show a wrong result would travel the same way (drawn as a picture, not a run).

### 9. The answer

> So why did one missing tool leave run B sure of something false? Because an agent is a model that knows only its context, and a loop that writes the world's answers into it.
> Run A's context held the test's answer. Run B's held only its own fix. Same model, different context.
> That's also why coding suits agents so well. Code comes with tests: a cheap and honest answer at every step. It's the reason Anthropic's engineers give.
> We've skipped a lot here: how models learn to call tools, planning, memory that lasts beyond one task, and teams of agents. Each of them still has to get what it knows into the context.
> So when you build an agent, or hand one a task, don't only ask how clever the model is. Ask what will tell it that it's wrong.

*Screen:* the two strips from chapter 1, as cards, now with their colours named once, small: grey "instructions", blue "the model's replies", green "tool results". A's green card with the red cross is outlined; the matching place in B's strip is empty. Then the loop picture from chapter 4 (model, our code, project, strip) settles in the middle. End card: the takeaway, and references: Anthropic, "Building effective agents" (Schluntz and Zhang, 2024); Anthropic, "Effective context engineering for AI agents" (2025); Claude API documentation, "How tool use works" and "Using the Messages API"; Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (2022); Willison, "I think 'agent' may finally have a widely enough agreed upon definition to be useful jargon now" (2025).

