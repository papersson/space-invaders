# It Said It Was Fixed

Status: locked after review round 6

## Argument

**Question.** We gave an LLM (Claude) a small Python project with one failing test, and the same request twice: fix report.py so that the test passes. Same model, same files, same request, same code around the model. Both runs took the same first four steps and made the same fix. Run A then took four more steps and replied "Fixed. ... All tests now pass." Run B replied "Fixed" right after its fix, saying its code now matched the test's expected values. We ran the test ourselves: after A it passes; after B it still fails. Three runs of each gave the same split. B's only difference was one missing tool, a way to run the test. What is an LLM agent, that taking away one tool leaves it sure of something false?

**Answer.** An agent is a model, some tools, and a loop. The model only reads text and writes text: on each call it reads its whole context (instructions, the request, and every tool call and tool result so far) and writes the next reply. When the reply is a tool call, the code around the model, not the model, runs the tool and adds the result to the context, then calls the model again; it stops when the model replies without a tool call. The model keeps nothing between calls (in run A, nine calls read from 1,423 up to 2,745 tokens each, 18,537 in all), so the context is its only memory of the task: it still knows what it learned in training (what a byte order mark is), but what it has tried and what came back, it knows only from the context. Run A's context received ground truth, the test's answer, a KeyError caused by an invisible byte order mark in the data file, and the next call acted on it: it read the data file, fixed the second bug, and the test passed. Run B's context never received a test result, so its own fix was the last word, and its "Fixed" was a reasonable conclusion from a context with no evidence against it. A more capable model, run the same way without the test tool, did better in two of three runs by the same mechanism: it read the data file unprompted, put the byte order mark into its own context, fixed both bugs, and said it had not been able to run the test; in the third, it asked for the file in a format our loop did not recognise, so the loop stopped. That is why agents work (each step can put ground truth into the context) and where they break down: where nothing checks the work, the model's guess stands, and in a longer task later steps build on it (compounding errors); and, in a loop like ours, the context only grows (Claude Code, a production agent, read 11,597 tokens on its first call and 123,192 over nine calls on the same task; longer contexts recall worse, which researchers call context rot); production agents summarize a long context (compaction), and whatever the summary drops, the model no longer knows.

**Takeaway.** An LLM agent is a model that picks each next step from its context, in a loop that runs those steps and writes the results back; about the task, it remembers nothing else. It can be trusted as far as ground truth reaches that context: before you trust an agent's "done", ask what would have told it that it was wrong.

**Wrong model.** The agent is a smart model that remembers what it has done and knows when it has succeeded; a better model makes a better agent by itself, and the code around it is plumbing.

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
7. Therefore run B: the same loop without run_tests. Its context never received the test's answer, so its "Fixed" stood. A more capable model did better only by reading the data file itself, and once failed because our loop missed its request. Therefore agents work where each step can put ground truth into the context, and break down where nothing checks the work (a wrong guess stands, and later steps build on it).
8. But there is a second way to break down: in a loop like ours the context only grows, and every call reads all of it (Claude Code: 11,597 tokens on its first call, 123,192 over nine calls; context rot). Production agents summarize it, but what a summary drops, the model no longer knows.
9. Therefore the answer.

Deviations from the canonical progression: the research gives plain call, then a single tool call (the function-calling round trip), then the loop (ReAct's Thought, Action, Observation), then workflows against agents, then failure modes. This script keeps that order, but replaces the standard weather-lookup and question-answering examples with one coding task run for real, because a coding task has a test, which lets the video show the loop's feedback working (run A) and missing (run B) with the same model. The loop is written with a plain-text tool-call format (a line of JSON), as in ReAct, instead of the API's structured tool_use blocks; the screen says so. Planning, long-term memory stores, multi-agent systems, how models are trained to call tools, and benchmark numbers are left out; the last chapter says so.

## Format

| Chapter | Format | Why |
|---|---|---|
| 1 | Narrated animation with real runs | The surprise is two contexts that start the same and end differently; both replies and our own test runs are real. |
| 2-5 | Narrated animation replaying real runs | Built up in order (bare model, one tool call, the loop) on one fixed picture: the model above, the project to the right, the context as a strip of cards along the bottom. Every card is a real message from a captured run. |
| 6 | Narrated animation from real counts | The strip turns into bars sized by the tokens each call read, stacked call by call. |
| 7 | Narrated animation replaying a real run | Run B's strip built under run A's, same scale. |
| 8 | Narrated animation with real numbers and a cited source | Claude Code's first-call context at the same scale; context rot is named and attributed, not simulated. |
| 9 | Narrated animation | Payoff: the two strips from chapter 1, now readable. |
| (not built) | Exercise | Run sims/agent.py's four versions (bare, one tool call, loop, loop without tests) on sims/project, then change the task or the tools and watch the context. The research names writing a small loop as the best way to learn it; offered, not added to the page. |
| (not built) | Reading | Anthropic, "Building effective agents" (2024) and "Effective context engineering for AI agents" (2025); Yao et al., ReAct (2022). |

## Ledgers

**Setups and payoffs.**
- The two replies that both begin "Fixed." (ch. 1) are explained by the two contexts (ch. 7) and in the answer (ch. 9).
- The shared first four steps (ch. 1) return as the replay (ch. 4) and as the point where A and B split (ch. 7).
- "B lacked one tool" (ch. 1) returns as B's tool list (ch. 7).
- "Nothing runs text" (ch. 2) is fixed by our code running tool calls (ch. 3).
- The unanswered second tool call (ch. 3) motivates the loop (ch. 4).
- The prediction (ch. 4) is answered by the KeyError (ch. 5).
- The invisible byte order mark (ch. 5) is what B never learned about (ch. 7).
- "The model chose to read the data file" (ch. 5) returns as "it had the tool, but no reason to" (ch. 7).
- "The context is its only memory" (ch. 6) is the reason B stopped (ch. 7) and the answer (ch. 9).
- "Every call reads all of it" (ch. 6) returns as the cost of a growing context (ch. 8).
- Ground truth (ch. 5) returns as why agents work (ch. 8) and in the answer (ch. 9).
- Run B's unchecked "Fixed" (ch. 7) returns as compounding errors (end of ch. 7).
- The staircase (ch. 6) returns as the second way agents break down (ch. 8).
- "The same model" (ch. 1) returns as the more capable model's runs (ch. 7) and in the answer (ch. 9).
- "Stop when it replies without one" (ch. 4) returns when the more capable model's request is missed and the loop stops (ch. 7).

**Vocabulary.**
| Term | First use | Meaning |
|---|---|---|
| LLM | ch. 1 | a model that reads text and writes what comes next (restated in ch. 2) |
| context | ch. 2 | everything the model reads on one call |
| tool | ch. 3 | ordinary code we wrote, which the model can ask us to run |
| tool call | ch. 3 | the model's request: a line of JSON naming a tool |
| tool result | ch. 3 | the tool's output, added to the context by our code |
| agent | ch. 4 | a model, tools, and a loop that runs its tool calls until it replies without one |
| workflow | ch. 5 | a sequence of steps fixed in advance by code |
| ground truth | ch. 5 | a tool result that reports what is actually so (the world's answer, not the model's guess); Anthropic's term |
| stateless | ch. 6 | keeps nothing between requests |
| compounding errors | ch. 7 | later steps building on an earlier, uncaught mistake |
| token | ch. 6 | the chunks of text a model reads; context size is counted in them |
| compaction | ch. 8 | summarizing a context that has grown long and continuing from the summary; Anthropic's term |
| context rot | ch. 8 | a model recalling less of its context as the context grows (Chroma, 2025; cited by Anthropic) |

**Numbers to remember.** Three of three: every run with the test tool passed, every run without it said "Fixed" and failed. Nine calls in run A, each re-reading the whole context (18,537 tokens in all). Supporting: a more capable model without the test tool, two of three.

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
> We reach the model through Claude's command-line tool, with that tool's own tools switched off, so text is all it can give back.
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

*Screen:* the bare strip clears back to its grey card, which widens as four tool names appear on it one by one (list_files, read_file, write_file, run_tests); the format line appears in the grey card, as the system prompt gives it: `{"tool": "read_file", "path": "report.py"}`. A small note under the format line: "a line of JSON here; real APIs give tool calls a structured form". A box labelled "our code" appears between the model and the project. The real run (captures/one_tool_1.json): the band sweeps the strip; a blue card `{"tool": "list_files"}` drops onto the strip, and an arrow carries it to "our code", which touches the project; a green card comes back and joins the strip, opening briefly to show "report.py sales.csv test_report.py". The band sweeps again, and a blue card `{"tool": "read_file", "path": "test_report.py"}` drops onto the strip; "our code" stays still; the card's outline pulses, unanswered.

### 4. The loop

> Therefore, a loop. Call the model. If its reply is a tool call, run the tool, and add the result to the context. Then call the model again.
> Stop when it replies without a tool call, or after twenty calls, in case it never does.
> That loop, with a model and some tools, is an agent. One common definition says just that: an LLM agent runs tools in a loop to achieve a goal.
> Here's run A, one call at a time. It lists the files, reads the test, and reads the code. And it spots a bug: the code adds the units to the price, where it should multiply them.
> It rewrites that line, then asks to run the test.
> Pause here, and make a prediction. The model found a real bug, and fixed it. Will the test pass?

*Screen:* "our code" turns into a loop: an arrow from the model's card down to "our code", on to the project, back into the strip, and up to the model. Beside it, the code card, exactly as in sims/agent.py (`def agent(task, tools, max_calls=20):` and its body: build the context from the task; for each call, call the model with the context, append its reply, parse a tool call; if there is none, return; otherwise run the tool and append its result), Then the replay of run A (captures/loop_1.json) on the strip, one call per pair of cards, the band sweeping before each blue card: list_files, read_file test_report.py, read_file report.py (its green card opens on the line `... + int(row["units"]) + float(row["unit_price"])`, the second plus highlighted), write_file report.py (the card opens on the same line with `*`). Then a blue card `{"tool": "run_tests"}` drops onto the strip, and everything stops: the arrow to "our code" waits. The pause holds for about three seconds.

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
> This isn't a quirk of our code. Anthropic's documentation says the same of its Messages API: it's stateless, so every request carries the whole context again.
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
> So this is why agents work, and the first way they break down. Each step can put ground truth into the context. Where nothing checks the work, the model's own guess has the last word.
> If that guess were one step in a longer task, the next call would read it as fact and build on it. Nothing here would catch that either. It's called compounding errors.
> Would a more capable model do better? We gave run B's setup to one, three times.
> Twice, with no way to run the test, it read the data file to check the sums by hand. It found the mark, and fixed both bugs. And it said plainly that it couldn't run the test.
> It did better the same way run A did: it put more ground truth into its own context.
> The third time, it asked for the data file in a format our code didn't recognise. Our loop saw no tool call, took the reply as final, and stopped.
> That failure wasn't the model's. It's chapter three again: the model can only ask, and our code decides what counts as asking, and what counts as done. The code around the model isn't plumbing.

*Screen:* the staircase folds back into run A's single strip of cards, which moves up; run B's strip is built beneath it card by card, cards aligned (captures/no_tests_1.json). B's grey card shows its tool list with run_tests missing. B's first four pairs line up under A's. At the fifth position, A's `run_tests` card and its green card with the red cross are outlined; under them, B's final blue card, "Fixed.", and then empty space where A's strip goes on. B's reply opens in full above its card (the real text, as in chapter 1). Then B's final card and the empty space are bracketed, the empty space labelled "no test result". Then the label "nothing checks the work" at the top left; for the compounding-errors lines, B's "Fixed." card is outlined in red and "compounding errors" appears under the label. Then, for the more capable model (captures/no_tests_strong_1.json to _3.json), A's and B's strips shrink upward and three short strips appear under them, labelled "more capable model": two whose blue cards include "read sales.csv", each followed by a green card with the red byte-order-mark marker, ending in "Fixed" and a check (our test run: OK), with the real reply's first line beside the first, "I fixed report.py, but I couldn't run the test because I have no tool to execute code. I checked the result by hand against sales.csv instead."; and one that ends after "read report.py" in a blue card showing its real reply, `<invoke_read_file> <parameter name="path">sales.csv</parameter> </invoke_read_file>`, then a red cross (our test run: FAIL). For the last line, the "our code" box from chapter 3 reappears beside that card, with the card's arrow stopping at it: "no tool call found → done".

### 8. The context grows

> The second way agents break down is in the staircase. In a loop like ours, the context only grows. Every step adds to it, and every call reads all of it.
> Here's the same task, run once by Claude Code, Anthropic's coding agent. It's the same command-line tool we've been calling the model through, now running its own loop, with its tools narrowed to match ours: read, edit, and run the test.
> Its first call read about eleven thousand six hundred tokens: its instructions, its tool descriptions, and our task.
> It found both bugs in nine calls, like run A. But it read those instructions again on every call, so in all it read over a hundred and twenty thousand tokens.
> And a longer task means more reading than its length suggests. Each new call re-reads everything before it, so twice the calls means more than twice the reading.
> The reading has a price beyond time. As a context grows, models get worse at recalling what's in it. Researchers call this context rot. Our runs are far too short to show it.
> Production agents, Claude Code among them, keep the context in check by summarizing it when it gets long. That's called compaction.
> But a summary is still the model's only memory. Whatever it leaves out, the model no longer knows.

*Screen:* the label "the context grows" at the top left. Run A's staircase from chapter 6, then its strip in token widths, at the chapter 6 scale; then Claude Code's first-call context (captures/claude_code_1.parsed.json) drawn at the same scale as a grey block that runs off the right edge; the view zooms out until it fits, and run A's whole strip becomes a short bar beside it. Its per-call counts as a staircase of nine rows (11,597 to 15,620, in amber; "9 calls"), the grey part of every row outlined, and the amber total, 123,192. For "twice the calls", run A's staircase with a second copy of its rows stacked on top, each longer, and the area beside it. Then the label "context rot · Hong, Troynikov and Huber (Chroma), 2025". For compaction, run A's strip (token widths) squeezes: every card after the instructions and the task folds into one short block labelled "summary" (a picture of the idea, not a run), and the label "compaction · Anthropic, 2025" appears. The strip then grows on from the summary.

### 9. The answer

> So why did one missing tool leave run B sure of something false? Because an agent is a model that picks each next step from its context, not from steps written in advance, as a workflow would.
> And a loop that runs those steps, and writes the results back in. About the task, the model remembers nothing else.
> Run A's context held ground truth from the test. Run B's held only its own fix. Same model, different context.
> The more capable model did better in just that way: it read the data for itself. And it said what it hadn't been able to check.
> That's also why coding suits agents so well, as Anthropic's guide points out. Code comes with tests: an answer the agent can check its work against at every step.
> We've skipped a lot here: planning, memory that lasts between tasks, and teams of agents. But each of those still reaches the model the same way: through its context.
> So when you build an agent, or hand one a task, don't only ask how clever the model is. Ask what will tell it that it's wrong.

*Screen:* the two strips from chapter 1, as cards, now with their colours named once, small: grey "instructions", blue "the model's replies", green "tool results". A's green card with the red cross is outlined; the matching place in B's strip is empty. Then the loop picture from chapter 4 (model, our code, project, strip) settles in the middle. End card: the takeaway, and references: Anthropic, "Building effective agents" (Schluntz and Zhang, 2024); Anthropic, "Effective context engineering for AI agents" (2025); Claude API documentation, "How tool use works" and "Using the Messages API"; Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (2022); Willison, "I think 'agent' may finally have a widely enough agreed upon definition to be useful jargon now" (2025); Hong, Troynikov and Huber, "Context Rot: How Increasing Input Tokens Impacts LLM Performance" (Chroma, 2025).

## Evidence

| Claim | Source |
|---|---|
| The project: report.py (revenue = units + unit_price, should be times), test_report.py (one unittest), sales.csv (7 rows; starts with a UTF-8 byte order mark, so csv.DictReader names the first column "﻿region" and `row["region"]` raises KeyError: 'region') | sims/project/; running `python3 -m unittest` there gives `KeyError: 'region'` |
| All runs: the same model (Claude, the claude command-line tool's default model on 2026-09-26), called once per step with `claude -p --tools ""` (the CLI's help, version 2.1.283: `--tools <tools...>` "Specify the list of available tools from the built-in set. Use "" to disable all tools"; research/verified_cli_flags.txt; a call asked to list its context named no tool definitions), so each call is a fresh process with no tools of its own; our code (sims/agent.py) sends the system prompt and the whole context on every call, parses a line of JSON as a tool call, and runs the tool itself | sims/agent.py, sims/run_all.sh; records in captures/*.json |
| Run A (the loop, four tools): 9 calls: list_files, read_file test_report.py, read_file report.py, write_file report.py (+ to *), run_tests (KeyError: 'region'), read_file sales.csv, write_file report.py (encoding="utf-8-sig"), run_tests (OK), reply "Fixed. ... All tests now pass."; our test run afterwards: OK | captures/loop_1.json; data/runs.txt |
| Run B (the loop without run_tests): 5 calls: the same first four steps, then reply "Fixed. ... now returns the correct totals per region, matching the expected values in test_report.py."; our test run afterwards: KeyError: 'region', FAILED | captures/no_tests_1.json; data/runs.txt |
| Three runs of each: loop 3 of 3 passed (9, 9 and 8 calls); without run_tests 3 of 3 replied "Fixed ..." and 3 of 3 failed our test run (5 calls each). The first run of each was chosen for the replay before any run was made | captures/loop_{1,2,3}.json, captures/no_tests_{1,2,3}.json; data/runs.txt |
| A more capable model (the command-line tool's model option), the loop without run_tests, three runs: two read sales.csv unprompted, fixed both bugs, and replied that they could not run the test and had checked the sums by hand ("I fixed report.py, but I couldn't run the test because I have no tool to execute code. I checked the result by hand against sales.csv instead."); our test run afterwards: OK. The third replied with a tool request in its own XML-like format (`<invoke_read_file>`), which our parser does not recognise, so the loop stopped after 4 calls; our test run: FAIL | captures/no_tests_strong_{1,2,3}.json; sims/run_stronger.sh; data/runs.txt |
| The bare model (one call, no tools described) replied with text that includes a made-up tool call "Tool: bash" and a find command; nothing ran; the test still fails | captures/bare_1.json |
| One tool call, no loop: call 1 asked for list_files; our code ran it; call 2 asked for read_file test_report.py, which nothing ran | captures/one_tool_1.json |
| Tokens read per call in run A: 1,423; 1,468; 1,637; 1,805; 2,027; 2,303; 2,446; 2,683; 2,745; total 18,537 (input + cache-creation + cache-read tokens reported by the API for each call) | captures/loop_1.json, "calls" |
| Of the 1,423 tokens on run A's first call, about 1,180 are notes the claude command-line tool adds to every call (working directory, date and similar), and about 240 are our system prompt and request: a one-character system prompt and prompt read 1,179 tokens | data/overhead.txt |
| Run A changed two lines of report.py (the plus sign; the open() call) | captures/loop_1.json, the two write_file calls |
| Claude Code on the same task: the same claude command-line tool, running its own loop, with tools limited to Read, Edit and `python3 -m unittest`: 9 model calls, 10 tool calls; tokens read per call 11,597 to 15,620, total 123,192 (its first-call context, read again on each of the nine calls, accounts for 104,373 of that); it edited the + to * (call 4), ran the test, got KeyError: 'region', inspected sales.csv's bytes, fixed the encoding, and the test passed; call 3 asked for three files at once, hence ten tool calls in nine model calls; its stream reports autocompact enabled | captures/claude_code_1.jsonl and .parsed.json; sims/run_claude_code.sh |
| "The model never executes anything on its own. It emits a structured request, your code (or Anthropic's servers) runs the operation, and the result flows back into the conversation." | Claude API docs, "How tool use works" (research/verified_primary_sources.md) |
| "The Messages API is stateless, which means that you always send the full conversational history to the API." | Claude API docs, "Using the Messages API" (research/verified_primary_sources.md) |
| "An LLM agent runs tools in a loop to achieve a goal." | Willison, 18 September 2025 (research/verified_primary_sources.md) |
| Stopping conditions such as "a maximum number of iterations" are common in agent loops (the code card's max_calls=20) | Anthropic, "Building effective agents" (2024); sims/agent.py |
| Workflows: "systems where LLMs and tools are orchestrated through predefined code paths"; agents: "systems where LLMs dynamically direct their own processes and tool usage"; agents need "ground truth" from the environment at each step; "higher costs, and the potential for compounding errors"; coding agents work well because "Code solutions are verifiable through automated tests" and "Agents can iterate on solutions using test results as feedback" | Anthropic, "Building effective agents" (Schluntz and Zhang, 19 Dec 2024) (research/verified_primary_sources.md) |
| Context rot: "as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases"; Anthropic says studies "uncovered the concept" and links Chroma's report, which named it | Anthropic, "Effective context engineering for AI agents" (29 Sep 2025); Hong, Troynikov and Huber (Chroma), "Context Rot" (14 July 2025) (research/verified_primary_sources.md) |
| Compaction: "taking a conversation nearing the context window limit, summarizing its contents, and reinitiating a new context window with the summary"; "In Claude Code, for example, we implement this by passing the message history to the model to summarize and compress the most critical details"; "overly aggressive compaction can result in the loss of subtle but critical context" | Anthropic, "Effective context engineering for AI agents" (2025) (research/verified_primary_sources.md) |
| Claude Code's first 4 calls read 49,369 tokens in all; its first 8 read 107,572 (twice the calls, 2.18 times the reading); on screen in ch. 8 for "twice the calls means more than twice the reading" | captures/claude_code_1.parsed.json (sums of its per-call counts) |
| Token counts are tokens read (input, cache creation and cache read), not dollars: with prompt caching, the repeated part of each call is billed at a discount, so the video makes no claim about cost | captures/*.json, "calls"; data/runs.txt |
| The loop of reasoning, actions and observations was introduced as ReAct | Yao et al., arXiv:2210.03629 (2022; ICLR 2023) |
| "Ground truth": "it's crucial for the agents to gain 'ground truth' from the environment at each step (such as tool call results or code execution) to assess its progress"; "compounding errors" | Anthropic, "Building effective agents" (2024) (research/verified_primary_sources.md) |
| The model knew the byte order mark from training: nothing in run A's context names it or the utf-8-sig fix before the model does | captures/loop_1.json (the context up to call 7) |
| Total tokens read grows faster than the number of calls: call n re-reads calls 1 to n-1, so doubling the calls more than doubles the total (arithmetic; run A: 9 calls, 18,537 tokens) | captures/loop_1.json |

## Review log

**Before round 1: the design principles** (research/principles.md). (1) The opening shows two real runs whose replies both begin "Fixed", and our own test run disagreeing with one, before any explanation. (2) The agent is built up from a bare model (ch. 2), to one tool call (ch. 3), to the loop (ch. 4), each step prompted by the previous version's visible failure, with an explicit "pause and make a prediction" before the first test run. (3) One central picture, the context as a strip of cards along the bottom, from chapter 1 to 9; it becomes token-sized bars and a staircase in chapter 6 and returns as cards. (4) Colours are bound to parts of the picture: grey instructions, blue the model's writing, green tool results, red a failing test, amber tokens read. (5) On screen: names of things, tool names, real quoted replies and real counts; no sentence captions. (6) One real case (run A) before any general statement; the wrong model is shown failing twice (the staircase against "it remembers", run B against "it knows when it has succeeded"). (7) Holds after reveals; chapter 9 says what is skipped and ends on a question to ask of any agent, not a recap.

**Round 1:** expert REVISE, editor PASS, student retold the question and answer correctly (lost "a few times", rated the opening 4/5).
- Expert, blocking: "the context is the model's only memory. Whatever isn't in it, the model doesn't know" (and ch. 9's "knows only its context") conflated memory of the task with knowledge from training, which the video itself contradicts (the model knew what a byte order mark is and how to skip it). Now narrowed everywhere: the context is the model's only memory of the task; ch. 6 says outright that it still knows what it learned in training, with the byte order mark as the example.
- Expert: "the API is stateless" now names the Messages API, as the source does, and glosses stateless ("keeps nothing between requests"); Anthropic's term "ground truth" is introduced in ch. 5 for the test's answer and used in chapters 8 and 9 instead of "the world's answer"; the Claude Code run now says its tools were narrowed to match ours; 11,597 is "about eleven thousand six hundred"; ch. 9's coding line now paraphrases the source more closely.
- Expert, not taken: re-titling the "Using the Messages API" reference. That is the page's own title, read today (research/verified_primary_sources.md); "Multiple conversational turns" is its section.
- Editor: the third failure mode ("errors stay"), which rested on a drawn picture rather than a run, is folded into the first: run B's unchecked guess is the real case, and compounding errors are named as what a longer task would do with it, attributed to Anthropic's guide; so chapter 8 now has two ways, not three, and objective 4 says so. The wrong model's second half is now refuted as directly as the first ("It looks as if the model knew it had succeeded. It didn't."). The closing list of skipped topics is shorter, with a clear referent. The number sentence in ch. 8 is now concrete ("a task twice as long means more than twice the reading"). "Steps" and "calls" are reconciled in ch. 6 ("nine calls in all: eight tool calls, and the final reply"), and ch. 4 replays "one call at a time".
- Editor, not taken: cutting context rot from the narration. Context limits are one of the canonical failure causes in both research reports; it stays as one attributed sentence, and the narration now says our runs are too short to show it, so it is not presented as something the video demonstrated. Cutting the source attributions in ch. 4 and ch. 9: the definition is the canonical one and is quoted verbatim ("to achieve a goal" stays, since it is the source's wording), and "coding suits agents" is a general claim the runs cannot show, so it keeps its source.
- Student: "LLM agent" was used in the opening question before any gloss; ch. 1 now says what one is in plain words ("a program that lets a model work on a task step by step") without giving away the mechanism. "Stateless" is glossed; the two Claude Code numbers are now in separate sentences; the closing list is shorter.

**Round 2:** expert REVISE, editor PASS, student retold the question and answer correctly (lost "once", at "nine calls" before it was counted; opening 4/5).
- Expert, blocking: "Anthropic's engineers call this context rot" misattributed the term. Checked (research/verified_primary_sources.md): Anthropic's essay says studies "uncovered the concept of context rot" and links Chroma's July 2025 report, which named it. The narration now says "Researchers call this context rot", and the screen and end card cite Hong, Troynikov and Huber (Chroma, 2025).
- Expert, blocking: about 1,180 of the first call's 1,423 tokens are notes the claude command-line tool adds to every call, which the "instructions" block hid. Measured (data/overhead.txt: a one-character system prompt and prompt read 1,179 tokens). Chapter 6 now says most of the first call is fixed text, "our instructions, and notes that the command-line tool we call the model through adds to every call", and the token-sized grey block is split into the two measured parts; chapter 2's model box is tagged "claude -p, tools off". Regenerating through the raw API was not possible: this environment has no API key, only the command-line tool.
- Expert, blocking: "a task twice as long means more than twice the reading" sat right after Claude Code's total, implying growth caused the gap with run A, when most of it is Claude Code's larger first-call context read again on each of its nine calls (11,597 x 9 = 104,373 of 123,192). The narration now names that cause, and the twice-as-long point is its own sentence about longer tasks.
- Expert: tokens are "the chunks of text a model reads"; the loop's cap of twenty calls is now spoken (a stopping condition, as Anthropic's guide recommends, and the code card's max_calls=20 is explained); "spots a bug", since there are two; Claude Code's ten tool calls in nine calls are on screen.
- Expert, not taken: adding "(or Anthropic's servers)" to "the model never executes anything on its own". That sentence is complete and verbatim in the source; the servers clause is about server-side tools this video doesn't use, which the model doesn't execute either.
- Editor: the workflow is now derived from a visible gap ("Nobody wrote that step in advance ... Ours would have stopped at the key error, with no step for what came next"); the second half of the wrong model ("a better model makes a better agent") is now named and answered in ch. 9 ("A smarter model might read more carefully. But it still can't see a test result that never arrives."); chapter 8 no longer carries three ideas: the first way agents break down, with compounding errors, now closes chapter 7 where run B shows it, and chapter 8 is only the growing context, starting from the staircase the viewer has already seen; the thesis sentence in ch. 9 is split in two; "stateless" is folded into one shorter sentence; the Anthropic attribution tags are cut from compounding errors (no longer attributed in narration) and shortened in ch. 9.
- Editor, not taken: cutting context rot or "Our runs are far too short to show it". Context limits are a canonical failure cause in both research reports, so one attributed sentence stays; saying plainly that our runs can't show it is the honesty the series asks for.
- Student: "nine calls" now arrives counted ("Run A called the model nine times: eight tool calls, then the final reply") before it's used.

**Round 3:** expert PASS, editor PASS, student retold the question and answer correctly (lost "a few times": "claude -p" against "Claude Code", the one-breath loop sentence, token counts with no sense of scale; opening 4/5). The gate is passed. Its should-fix items are applied once below, and round 4 decides the lock.
- Reviewer independence: the reviewers run as `claude -p` in the tutor folder, with file tools, and the round 3 expert says it read the capture files and the earlier expert reviews (and cites the concurrent student review). Its checks against the data are useful, but it was not a fresh context in the sense the process asks for. Round 4 is run from an empty scratch folder, so the lesson's files, earlier reviews and review log are not at hand.
- Expert: chapter 8 now says Claude Code is the same command-line tool the video has been calling the model through, running its own loop, which the student had also tripped on.
- Expert, not taken (NIT): a "page of text" scale for the token counts. The staircase shows relative size, which is what the argument uses, and a pages figure would be a new unmeasured number.
- Editor: "request" named both the task and the model's tool call; the task is now always "the task", and a tool call is never a "request" in the narration. Claude Code's "10 tool calls" is off the screen (it asked for three files in one call), so "nine calls, like run A" stands alone. Compounding errors is now marked as inference ("If that guess were one step in a longer task, the next call would read it as fact and build on it. Nothing here would catch that either."). The workflow chips are tagged "scripted (not run)"; the chapter 7 label that repeated the narration now marks the empty slot, "no test result"; the superlinear sentence gives its reason first; the loop sentence in ch. 4 is split in two (the student's point too); the answer says the model picks each step "from its context, not from a script", tying the workflow distinction into the answer, since no student retelling had carried it.
- Editor: "A smarter model might read more carefully. But it still can't see a test result that never arrives" was asserted, not shown. We ran it (sims/run_stronger.sh, captures/no_tests_strong_*.json): run B's setup, three runs with a more capable model. Two of three read sales.csv unprompted, found the byte order mark, fixed both bugs, passed our test run, and said they could not run the test and had checked by hand; the third answered in its own tool-call format, which our parser did not recognise, so the loop stopped and the test still failed. The line was wrong in spirit, and chapter 7 now reports these runs: a more capable model did better by the same mechanism (putting more ground truth into its own context) and said what it hadn't checked, and its one failure came from our loop, which also answers the wrong model's "the code around it is plumbing". Chapter 9 calls back to it.
- Editor, not taken (NIT): cutting the twenty-call cap from the narration. The round 2 expert asked for it, since the code card shows it and it is a standard stopping condition.
- Editor, not taken (NIT): a proportional split of Claude Code's 11,597 first-call tokens. It was not measured, and the narration makes no claim about the split.

**Round 4 (final round, run from an empty folder):** expert REVISE, editor PASS, student retold the question and answer correctly (lost "a few times": the command-line tool's notes arriving in chapter 6 with no setup, "with one", and the pile of token numbers; opening 4/5). Not locked: the blocking item is fixed below and round 5 decides.
- Expert, blocking: "the context only grows" was stated of agents in general, but production harnesses, Claude Code included, summarize a long context (compaction). Checked in Anthropic's context-engineering essay (research/verified_primary_sources.md), and Claude Code's captured stream reports autocompact enabled. Chapter 8 now scopes the claim ("In a loop like ours, the context only grows"), names compaction as what production agents do, and ties it back to the thesis: a summary is still the model's only memory, and whatever it leaves out, the model no longer knows (the essay warns of exactly that loss).
- Expert: "slower and costlier" dropped. The counts are tokens read, including cache reads, which providers bill at a discount, so the video makes no dollar claim; the evidence table says so. Compaction now covers the "context management" gap the expert saw in the skipped list, so the list itself is unchanged. The note that a line of JSON stands in for the APIs' structured tool calls moved to chapter 3, where the format first appears. The evidence table now states that Claude Code also fixed the plus sign (call 4) and why it made ten tool calls in nine model calls.
- Expert, not taken (NIT): "tool use" instead of "tool call". Both are standard; "tool call" is the more common across vendors and in the definition quoted (Willison), and the video uses one term throughout.
- Editor: the stateless sentence now says "context", not "conversation" (one name per concept); the answer's workflow callback now names the workflow.
- Editor, not taken: dropping the label "compounding errors" and cutting context rot. Both are canonical failure modes in the research; each is one sentence, marked as inference or as unshown, and naming them gives the viewer the words the sources use.
- Student: the command-line tool is now introduced in chapter 2, where the model first appears ("We reach the model through Claude's command-line tool, with that tool's own tools switched off"), so its notes in chapter 6 and its own loop in chapter 8 have a setup; "with one" is rephrased.

**Round 5:** expert REVISE, editor REVISE, student retold the question and answer correctly (lost "a few times": the command-line tool's notes, the byte order mark's backstory, the unrecognised format; opening 4/5).
- Expert, blocking, not taken: "`--tools` is not a real flag of the Claude Code CLI ... passing an empty string is not documented". It is: `claude --help` (version 2.1.283, saved in research/verified_cli_flags.txt) lists `--tools <tools...>` "Specify the list of available tools from the built-in set. Use "" to disable all tools", and the bare model, asked to list its context, named no tool definitions. The evidence table now quotes the help text, so the next reviewer can see the check.
- Editor, blocking (and the expert's should-fix on the same beat): the more capable model's third run, stopped by our parser, was a failure the chapter never placed. Chapter 7 now states the first way agents break down before the more capable model's runs, and names the third run for what it is: not the model's failure but our code's, "chapter three again: the model can only ask, and our code decides what counts as asking, and what counts as done". That answers the wrong model's "the code around it is plumbing" instead of adding a third way to break down.
- Expert, should fix: verify the titles, authors and quotes on the end card. They were read from the live pages in this session (research/verified_primary_sources.md, including "Using the Messages API" as that page's title); the reviewer, run from an empty folder, could not reach them.
- Expert, NIT: "is the whole agent" is now "is an agent". Not taken: quoting the "(or Anthropic's servers)" clause (as in round 2).
- Student: the list of skipped topics is unchanged (three items, each said once, as the research's "leave out" list names them).

**Round 6:** expert PASS, editor PASS, student retold the question and answer correctly (lost "a few times": "tools switched off" in ch. 2 before tools are defined, and the dense stretch in ch. 7; opening 4/5). The gate holds again after the blocking fixes from rounds 4 and 5, so the script is locked. The student's retellings across all six rounds carried objectives 1 to 3 and both ways agents break down, but none mentioned the workflow distinction; it stays in chapters 5 and 9 as a named contrast, and is the first revision candidate if the learner's notes point there.
- Revision candidates, not applied (round 6 should-fix items and NITs; the narration is locked): the expert asks for the "real APIs give tool calls a structured form" caveat to be spoken in ch. 3, not only shown (the screen note stays, made more prominent); "over a hundred and twenty thousand" could be "about a hundred and twenty-three thousand"; the editor would cut or de-number the twenty-call cap, and ground context rot and compaction in the runs or cut them; "the world's answer" and "ground truth" share one sentence in ch. 5; the end card should show only a short line, not the narration.

**The design principles at the lock** (research/principles.md):
1. Question first: chapter 1 shows the two runs, both replies beginning "Fixed", and our own test run disagreeing with one, before any explanation; the question is spoken at the end of the chapter and answered only in chapter 9. Student reviewers rated the opening 4 of 5 in every round.
2. Discovery order: bare model (nothing runs its text), one tool call (the second request is left hanging), the loop; each built from the previous version's visible failure. One explicit "Pause here, and make a prediction" before the first test run (ch. 4, with a hold), answered by the KeyError.
3. One central picture: the context as a strip of cards, from chapter 1 to 9; it becomes token-sized bars and a staircase (ch. 6), returns as cards for run B (ch. 7), and as bars for Claude Code and compaction (ch. 8).
4. Continuity and colour: grey instructions, white task, blue the model's writing, green tool results, red a failing test, amber tokens read; the same geography (model above, our code and the project to the right, the strip along the bottom) in every chapter from 2 on.
5. Minimal text: labels are names (tools, files), real counts and real quoted replies; the few short labels are names of ideas ("nothing checks the work", "context rot · Hong et al. 2025"); no sentence captions. To be checked again on the frames.
6. Concrete first, wrong model shown failing: one real run (A) before every general statement; "it remembers" fails against the staircase (every call re-reads everything), "it knows when it has succeeded" against run B, "a better model by itself; the code is plumbing" against the more capable model's runs (better only by gathering ground truth; its one failure was our parser).
7. Breathing room and honesty: holds after reveals (narration.json); the script says what it can't show (context rot "far too short to show", compaction drawn as a picture), what it skips, and ends on a question to ask of any agent rather than a recap.

**Frame review after the first full render** (a fresh `claude -p` context with 30 pages of frames, one near the end of every sentence, the script with its evidence, the run summaries and the code checks; research/frame_review/): FRAMES: FIX, with 1 MUST FIX, 3 SHOULD FIX and 4 NITs. Every number, quoted reply, code line and citation on screen matched the evidence. The narration is unchanged; all fixes are on screen.
- MUST FIX: chapter 8 held one frame across four sentences, including "twice the calls means more than twice the reading", which the screen note had promised to show with a hypothetical doubled staircase. It now shows Claude Code's own counts: brackets on its first 4 calls (49,369 tokens) and first 8 (107,572), real data rather than a hypothetical, added to the evidence table; "context rot" appears on its own sentence, is marked on the next, and "not shown by these runs" appears when the narration says so.
- SHOULD FIX: in chapter 3, the arrow from the tool call to "our code" vanished before the end of the sentence that says who ran the tool; the arrows (tool call to our code, our code to the project, the result back to the strip) now stay through "Notice who ran it". The byte order mark's marker used red, which means a failing test; it is now white. In chapter 7, "no tool call found → done" now appears with the sentence that says it, not one later.
- NITs applied: chapter 3 lists the tool names first and shows the JSON form when the narration introduces it; run B's reply is abridged the same way in chapters 1 and 7. Not applied: the Claude Code staircase keeps its own teal for "everything since" (its capture can't be split into tool calls and results, so it shouldn't borrow blue and green, and amber means counts); the chapter 9 legend says "the model's writing", which is more exact than the screen note's "the model's replies", since tool calls are writing too.
