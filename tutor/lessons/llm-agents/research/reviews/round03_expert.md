I read through the script against the underlying data (`captures/*.json`, `data/runs.txt`, `data/overhead.txt`, `sims/agent.py`, `sims/project/*`, and the primary-source quotes in `research/verified_primary_sources.md`), and against the prior two review rounds already on file (`research/reviews/round0{1,2}_expert.md`), which had already caught and fixed several real problems (the context-rot misattribution, the conflation of task-memory with training knowledge, the "twice the calls" placement, the undisclosed CLI overhead, etc.). All of those fixes verify correctly against the source data — the token arithmetic checks out exactly (1,423→2,745 summing to 18,537; 11,597×9=104,373; total 123,192), the BOM is genuinely `ef bb bf` before `region`, the CSV math (27.5/19.75/40.0/17.0) checks out under multiplication, and every quoted reply matches the capture files verbatim.

My own pass surfaced one new issue worth fixing and a couple of minor polish items.

## SHOULD FIX

**Quote (ch. 8):** *"Here's the same task, run once by Claude Code, Anthropic's coding agent, with its tools narrowed to match ours: read, edit, and run the test."*

**What's wrong:** This is introduced as if it's a different product from the "claude -p, tools off" box tagged in chapter 2 — but per `sims/run_claude_code.sh`, both are literally invocations of the same `claude` command-line tool; chapter 2 runs it with `--tools ""` (its own agent loop disabled, driven externally by `sims/agent.py`), and chapter 8 runs it with `--tools "Read,Edit,Bash"` (its own native agent loop, narrowed). The script never reconnects these, so a viewer has no way to know chapter 8 is "the same tool with its loop switched back on" rather than an unrelated system — and the round-3 student reviewer independently hit exactly this confusion ("Is 'claude -p' the same thing as 'Claude Code'... or two different products?"). It also undersells the point: the real comparison is toy external loop vs. the same model's own built-in loop, which is a stronger, more precise claim than "our homemade thing vs. a production agent."

**Corrected wording:** *"Here's the same task, run by Claude Code — the same `claude` command-line tool from chapter 2, but now with its own tools turned back on, narrowed to match ours: read, edit, and run the test."* (and pay off the chapter 2 tag explicitly rather than only via the shared name)

## NIT

**Quote (ch. 6):** *"The first call read about fourteen hundred."* … *"the ninth read about twenty-seven hundred."*

Not wrong (1,423 and 2,745 round correctly), but a viewer has no anchor for whether ~1,400–2,700 tokens is a little or a lot of text — the same gap the round-3 student review flagged. Not essential to the argument (which is about relative growth, not absolute scale), so optional: a half-clause like *"about a page of text"* somewhere in chapter 6 would help without adding a new claim to verify.

## What holds up (checked, not just trusted)

- Every quoted model reply, every step sequence, and every token count matches the capture files exactly, including the "3 of 3" replication claim and the two-bugs-not-one framing in chapter 4/5.
- All four attributed quotes (tool-use docs, Messages API statelessness, Willison's definition, "Building effective agents" on ground truth/workflows/compounding errors/coding agents) are verbatim against `research/verified_primary_sources.md`, correctly scoped (e.g., "Messages API" not "the API" generally), and the context-rot attribution correctly credits Chroma via "researchers," not Anthropic.
- The BOM/`utf-8-sig`/`csv.DictReader` explanation is textbook-correct, and the "second plus" bug identification is the exact token in `report.py`.
- The superlinear-growth claim ("twice the calls means more than twice the reading") is not just plausible but provably true given the stated append-only context model, and it's now correctly detached from the Claude Code total (which is correctly attributed to a large first-call context re-read nine times, 104,373 of 123,192).
- Nothing overclaims optimality or generality beyond what's shown; chapter 9 explicitly scopes out what's skipped (planning, cross-task memory, multi-agent), and the JSON-tool-call simplification is flagged on-screen as non-standard versus real structured tool-use APIs.

VERDICT: PASS
