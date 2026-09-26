I reviewed the script against the verified primary-source quotes in `research/verified_primary_sources.md`, checked the arithmetic in every numeric claim, and cross-checked the on-screen claims against the underlying capture files described in the evidence table.

## Findings

**BLOCKING** — Chapter 6 (restated as the thesis in Chapter 9)
> "So the context is the model's only memory. Whatever isn't in it, the model doesn't know."
> (Chapter 9: "an agent is a model that knows only its context")

This conflates *episodic memory* (what happened in this session) with *knowledge* (what the model learned in training), and the video's own Chapter 5 disproves the literal claim: the model recognizes the byte-order-mark problem and fixes it with `encoding="utf-8-sig"` — a piece of Python/encoding knowledge that was never in its context (no tool result told it "this is a BOM" or "use utf-8-sig"). That fix came from pretraining, not from anything "in" the context. As worded, a viewer would conclude the model has no capability at all beyond what's spoon-fed to it, which the video itself shows is false.
**Fix:** narrow the claim to what's actually being argued — memory of *this task*, not knowledge in general. E.g.: "So the context is the model's only memory of this task — what it's tried, what came back. Whatever isn't in it, the model has no way to recall, even if it still knows plenty from training." Apply the same narrowing to the Chapter 9 line ("a model that remembers only its context" rather than "knows only its context").

**SHOULD FIX** — Chapter 6
> "Anthropic's API documentation says the API is stateless: you always send the full conversation."

The verified source is specifically about the **Messages API** ("The Messages API is stateless, which means that you always send the full conversational history to the API."). Saying "the API" generically is a step away from the canonical claim and reads as broader than the source supports.
**Fix:** "Anthropic's documentation says the Messages API is stateless: you always send the full conversation history."

**SHOULD FIX** — Chapters 5 and 8
> "each step can put the world's answer into the context" / "So we ran the test ourselves"

The canonical term from "Building effective agents" is **ground truth**, used verbatim in the source ("it's crucial for the agents to gain 'ground truth' from the environment at each step"). The script never uses this term even though it's exactly the standard vocabulary a professor would want reinforced, and the whole video is an extended illustration of it.
**Fix:** work "ground truth" into Chapter 5 or 8 explicitly, e.g., "That result is the agent's ground truth — the environment's answer, not the model's guess," with the on-screen citation attached there instead of only at "context rot."

**SHOULD FIX** — Chapter 8
> "Here's the same task, run once by Claude Code, a production agent."

Per the evidence table, Claude Code's tools were deliberately restricted to Read, Edit, and `python3 -m unittest` to make the comparison fair to the toy loop. The narration doesn't disclose this, so a viewer may think Claude Code's real, much larger toolset was in play, or wonder why a "production agent" only ever used three tools.
**Fix:** add a half-sentence: "...run once by Claude Code, a production agent, its tools narrowed to match ours: read, edit, run the test."

**NIT** — Chapter 9
> "Code comes with tests: a cheap and honest answer at every step."

Loose paraphrase of the source ("Code solutions are verifiable through automated tests; Agents can iterate on solutions using test results as feedback"). Not wrong, but drifts from the citation's own language for a line doing a lot of argumentative work.
**Fix (optional):** "Code comes with tests: a verifiable answer at every step, that the agent can iterate against."

**NIT** — End references
> Claude API documentation, "How tool use works" and "Using the Messages API"

Per the research notes, "Using the Messages API" is a section heading inside the page at `/build-with-claude/working-with-messages` (titled "Multiple conversational turns" at the subsection level) — worth confirming the page's actual top-level title before it goes in a references card, since a viewer may search for that exact title and not find it.

**NIT** — Chapter 8
> "Its first call read about eleven and a half thousand tokens"

11,597 rounds more naturally to "about eleven thousand six hundred" — "eleven and a half thousand" undershoots by ~100 tokens. Trivial, but the rest of the script's rounding is careful (18,537 → "eighteen and a half thousand" is a good rounding), so this one line is inconsistent with that standard.

## What holds up
The core arithmetic checks out exactly: the nine per-call token counts in run A sum to 18,537 as stated; the "two lines changed" claim matches the two `write_file` diffs; the "3 of 3" replication claims match the evidence table; the BOM/`csv.DictReader`/`utf-8-sig` explanation is textbook-correct; the workflow-vs-agent distinction and the Willison and tool-use-API quotes are verbatim and correctly attributed; "context rot" is confirmed as the essay's own term, not a misattribution.

VERDICT: REVISE
