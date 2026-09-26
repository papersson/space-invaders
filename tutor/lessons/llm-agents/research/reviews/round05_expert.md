I attempted to independently verify the four citation-dependent claims (CLI flag syntax, two Anthropic doc quotes, the Willison quote, and the Chroma authorship) using web search, but this environment has WebSearch/WebFetch permission denied for me and for the sub-agents I dispatched. Two of the three research agents came back and explicitly reported they had no working tool and refused to guess. The third (claude-code-guide) returned a confident-sounding answer, but since it hit the same permission wall, I cannot certify it was actually checked against live docs rather than produced from training memory. I'm flagging this limitation rather than passing off unverified claims as checked. Below is my review, drawing on my own domain knowledge; items I could not confirm against a live source are marked accordingly and should get a final check before the video ships.

## Findings

**BLOCKING** — `sims/agent.py, sims/run_all.sh` note in Evidence table; screen direction in Ch. 2 ("claude -p, tools off")
> "called once per step with `claude -p --tools \"\"`"

To my knowledge `--tools` is not a real flag of the Claude Code CLI's non-interactive mode, and passing an empty string is not documented syntax for suppressing tool use — the flag that controls tool availability takes tool *names*, not an on/off switch. This isn't just a documentation nit: Chapter 2's entire experiment rests on the claim that this specific invocation left the model with zero ability to act. If the flag as written doesn't do what's claimed, the "bare model" and "one tool call" and "loop" captures may not have been produced under the conditions the narration asserts. Before this ships, run `claude -p --help` and confirm the exact flag actually used to produce `captures/bare_1.json`, `one_tool_1.json`, and `loop_1.json`/`no_tests_1.json`, and correct the Evidence table (and any on-screen command text, if the real flag appears there) to match. **Corrected wording:** state the actual verified flag (e.g. something like `claude -p --disallowedTools "*"`, but confirm this precisely rather than taking my word or the sub-agent's word for it).

**SHOULD FIX** — Ch. 7 script text
> "The third time, it asked for the data file in a format our code didn't recognise. Our loop saw no tool call, and stopped. So this is why agents work, and the first way they break down."

The third "more capable model" run is a different failure mode than the other two anecdotes in this beat: runs 1 and 2 illustrate the ground-truth thesis (the model checked its own work), but run 3 is a harness/parsing failure — the model asked for something in a format the code couldn't parse, which has nothing to do with ground truth or overconfidence. Placing it immediately before "so this is why agents work, and the first way they break down" invites the viewer to read it as one more instance of the same lesson, when it's actually a distinct failure class (interface brittleness between model output and the code that must parse it). **Corrected wording:** add a clause distinguishing it, e.g. "...Our loop saw no tool call, and stopped — a different kind of failure: not the model's confidence, but our code's ability to understand it. So [the ground-truth point] is why agents work, and the first way they break down [is the earlier one]."

**SHOULD FIX (verify before publishing)** — End-card references and in-narration attributions
> "Anthropic's documentation puts it plainly: the model never executes anything on its own." (citing "How tool use works")
> "Anthropic's documentation says the same of its Messages API: it's stateless..." (citing "Using the Messages API")
> Willison, "I think 'agent' may finally have a widely enough agreed upon definition to be useful jargon now" (2025)
> Hong, Troynikov and Huber, "Context Rot..." (Chroma, 2025)

I have moderate, not certain, recollection that these titles/authors/quotes are correct, but I could not check them against the live pages in this session (tool access was denied), and one of my own sub-agents flagged a specific, plausible failure mode worth checking: that the statelessness quote may actually live on a "Context windows" doc rather than one titled "Using the Messages API." Given this is a citations list a knowledgeable viewer could click through, get each exact title, URL, and quote confirmed against the live source before this ships — a wrong doc title or misattributed author is exactly the kind of thing that undermines credibility with an audience capable of checking. No corrected wording to offer until verified; this is a "go check it" item, not a "here's the fix."

**NIT** — Ch. 3 script text
> "Anthropic's documentation puts it plainly: the model never executes anything on its own."

If the full quote is (as the Evidence table itself gives it) "...your code (**or Anthropic's servers**) runs the operation...", the script's paraphrase silently drops the server-executed-tools case. It doesn't make the sentence wrong for this example (nothing here uses a server-side tool), but a precise citation shouldn't trim a clause that changes what the source is actually claiming. **Corrected wording:** either quote the full sentence, or add "(here, that's our own code, though Anthropic's servers run some tools directly)."

**NIT** — Ch. 4 script text
> "That loop, with a model and some tools, is the whole agent."

This is fine as the minimal working definition the video builds up to, and Chapter 9 does walk it back ("We've skipped a lot here: planning, memory that lasts between tasks, and teams of agents"), so it's not left uncorrected. Still, "the whole agent" is a stronger claim than the video ultimately defends. **Corrected wording:** "the whole of *this* agent" or "the core of an agent" would better match the hedged framing that comes later.

## What I checked and found solid
Every arithmetic claim verifies exactly: the nine per-call token counts in Ch. 6 sum to 18,537; the Claude Code totals (11,597 first call, 123,192 total, 9 calls) match the evidence; the call counts for runs A (9) and B (5) and the "four more steps" framing in Ch. 1 are internally consistent throughout. The core technical narrative — statelessness, context-as-memory, ground truth, workflows vs. agents, compounding errors, context rot, compaction — uses standard terminology correctly and consistently, matches the cited Anthropic concepts as I know them, and is honestly hedged where it should be (explicitly noting the runs are "far too short to show" context rot, that compaction is "a picture of the idea, not a run," and that cost is never claimed from token counts). The BOM/encoding explanation is technically correct.

VERDICT: REVISE
