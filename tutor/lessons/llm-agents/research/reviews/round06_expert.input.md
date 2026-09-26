You are a professor who has taught this material for years. Below is the script of a short narrated explainer video, with a note of what is on screen at each moment, followed by the list of numbers it uses and where each comes from. Review it for correctness and canonicity. You are the only domain expert who will see it before it is produced, so be exacting. Report every problem with: severity (BLOCKING = wrong, misleading, or non-canonical in a way a professor would object to; SHOULD FIX = imprecise, a missing caveat, non-standard terminology; NIT), the exact quote, what is wrong, and the corrected wording. Check every factual and numerical claim including arithmetic and units; that terminology and notation match the standard sources and simplifications teach nothing false; whether anything essential is missing or anything peripheral gets too much weight; and overstated claims about optimality, generality and real systems. End with "VERDICT: PASS" if there are no BLOCKING items, otherwise "VERDICT: REVISE".


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
| Token counts are tokens read (input, cache creation and cache read), not dollars: with prompt caching, the repeated part of each call is billed at a discount, so the video makes no claim about cost | captures/*.json, "calls"; data/runs.txt |
| The loop of reasoning, actions and observations was introduced as ReAct | Yao et al., arXiv:2210.03629 (2022; ICLR 2023) |
| "Ground truth": "it's crucial for the agents to gain 'ground truth' from the environment at each step (such as tool call results or code execution) to assess its progress"; "compounding errors" | Anthropic, "Building effective agents" (2024) (research/verified_primary_sources.md) |
| The model knew the byte order mark from training: nothing in run A's context names it or the utf-8-sig fix before the model does | captures/loop_1.json (the context up to call 7) |
| Total tokens read grows faster than the number of calls: call n re-reads calls 1 to n-1, so doubling the calls more than doubles the total (arithmetic; run A: 9 calls, 18,537 tokens) | captures/loop_1.json |

