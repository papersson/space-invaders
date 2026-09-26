# Primary sources checked in this session (2026-09-26)

Each quote below was read from the source itself (WebFetch of the page), not recalled.

## Anthropic, "Building effective agents" (Erik Schluntz and Barry Zhang, published Dec 19, 2024)
https://www.anthropic.com/engineering/building-effective-agents
- "Workflows are systems where LLMs and tools are orchestrated through predefined code paths."
- "Agents, on the other hand, are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks."
- "They are typically just LLMs using tools based on environmental feedback in a loop."
- "During execution, it's crucial for the agents to gain 'ground truth' from the environment at each step (such as tool call results or code execution) to assess its progress."
- "The autonomous nature of agents means higher costs, and the potential for compounding errors."
- On coding agents: "Code solutions are verifiable through automated tests; Agents can iterate on solutions using test results as feedback; The problem space is well-defined and structured; and Output quality can be measured objectively."
- "it's also common to include stopping conditions (such as a maximum number of iterations) to maintain control."

## Anthropic API docs, "How tool use works"
https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works
- "The model never executes anything on its own. It emits a structured request, your code (or Anthropic's servers) runs the operation, and the result flows back into the conversation."
- "The model can't run your code, so every tool call is a round trip: the model asks, you execute, you report back, the model continues."
- The loop: "while `stop_reason == "tool_use"`, execute the tools and continue the conversation." Step 4: "Send a new request containing the original messages, the assistant's response, and a user message with the `tool_result` blocks."

## Anthropic API docs, "Using the Messages API", section "Multiple conversational turns"
https://platform.claude.com/docs/en/build-with-claude/working-with-messages
- "The Messages API is stateless, which means that you always send the full conversational history to the API."

## Simon Willison, "I think "agent" may finally have a widely enough agreed upon definition to be useful jargon now" (18 September 2025)
https://simonwillison.net/2025/Sep/18/agents/
- "An LLM agent runs tools in a loop to achieve a goal."

## Anthropic, "Effective context engineering for AI agents" (published Sep 29, 2025)
https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- "as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases." (the essay calls this context rot)
- "Context, therefore, must be treated as a finite resource with diminishing marginal returns."
- "An agent running in a loop generates more and more data that _could_ be relevant for the next turn of inference"
- "Compaction is the practice of taking a conversation nearing the context window limit, summarizing its contents, and reinitiating a new context window with the summary."

## Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (arXiv:2210.03629, 6 Oct 2022; ICLR 2023)
https://arxiv.org/abs/2210.03629
- Generates "both reasoning traces and task-specific actions in an interleaved manner".
- ReAct "overcomes issues of hallucination and error propagation prevalent in chain-of-thought reasoning by interacting with a simple Wikipedia API."

## Kwa et al. (METR), arXiv:2503.14499 (submitted 18 March 2025)
https://arxiv.org/abs/2503.14499
- 50% time horizon: "The time humans typically take to complete tasks that AI models can complete with 50% success rate."
- "Current frontier AI models such as Claude 3.7 Sonnet have a 50% time horizon of around 50 minutes."
- "Frontier AI time horizon has been doubling approximately every seven months since 2019, though the trend may have accelerated in 2024."
- Title: the web-research pass reports "Measuring AI Ability to Complete Long Tasks"; the arXiv page fetched today gives "Measuring AI Ability to Complete Long Software Tasks" (probably a later version's title). Not used on screen unless re-checked.
