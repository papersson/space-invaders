I reviewed the script against the evidence table, checked every arithmetic sum, cross-referenced each attributed quote against the source material listed, and read the screen directions for internal consistency with the narration. This is an unusually well-sourced script — every specific number traces to a captured run, and the video is careful to hedge claims it can't fully back (e.g., calling context rot "far too short to show," labeling the compaction visual "a picture of the idea, not a run"). I found no factual, arithmetic, or attribution errors. Two items are worth fixing before production.

## Findings

**SHOULD FIX** — Section 3
> "We also tell the model how to ask for one: reply with one line of JSON that names the tool. That message is called a tool call."

The important caveat that this is *not* how Claude's real tool-use API works is relegated to a small on-screen note ("a line of JSON here; real APIs give tool calls a structured form") and never spoken. A viewer who isn't reading every on-screen annotation — or who's only listening — will walk away thinking Anthropic's actual tool-calling mechanism is "the model writes a JSON line into its text output and something parses it out," when in fact the Messages API returns tool calls as structured `tool_use` content blocks (id/name/input), not free text to regex out of a reply. The video is otherwise careful to flag toy-vs-real distinctions verbally (e.g., contrasting the custom loop with real Claude Code in ch. 8), so this one should get the same treatment given how central "who decides what counts as a tool call" becomes later (ch. 3's closing line, reused in ch. 7 for the XML-format failure).

Corrected wording (add a spoken line, doesn't need to lengthen the shot much):
> "...reply with one line of JSON that names the tool. That message is called a tool call — in Claude's real API it's a structured field, not text; we're parsing it out of plain text ourselves because we've kept the CLI's own tools switched off."

**NIT** — Section 8
> "But it read those instructions again on every call, so in all it read over a hundred and twenty thousand tokens."

The measured total is 123,192. "Over a hundred and twenty thousand" is true but looser than it needs to be, and reads oddly next to the otherwise tight rounding elsewhere in the script ("about eighteen and a half thousand" for 18,537). Consider "about a hundred and twenty-three thousand."

Everything else checked out:
- All token arithmetic verifies exactly (run A's nine per-call counts sum to 18,537; Claude Code's 11,597 first call and 123,192 total are consistent with the per-call range given).
- Every direct/near-direct quote (statelessness, "ground truth," the workflow/agent split, context rot, compaction, "the model never executes anything on its own," Willison's definition) matches the cited source's meaning without distortion, and each is appropriately hedged ("one common definition," "what Anthropic's guide... calls") rather than presented as sole authority.
- The "twice the calls means more than twice the reading" claim (ch. 8) is actually the *correct*, general form of the argument — it follows from context length being non-decreasing across calls, and doesn't overclaim a specific growth rate (e.g., quadratic) that only 9 data points wouldn't license.
- The workflow-vs-agent contrast, the run A/run B comparison, and the stronger-model ablation are all scoped to what was actually run (3 runs each, first run replayed) and never generalized beyond that.
- No optimality or real-system overclaims: the closing message is an epistemic question ("what will tell it that it's wrong"), not a solution claim.

VERDICT: PASS
