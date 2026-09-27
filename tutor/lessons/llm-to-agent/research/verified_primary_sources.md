# Primary sources checked in this session (2026-09-27)

Each quote below was read from the source itself (WebFetch of the page, or the file itself), not recalled, unless marked otherwise.

## ChatGPT's launch (30 November 2022)
- OpenAI, "Introducing ChatGPT", https://openai.com/index/chatgpt/ . The page answers 403 to direct fetches from here; its date and wording were read from the search engine's copy: "a model called ChatGPT which interacts in a conversational way".
- Confirmed by TechCrunch, "ChatGPT launched three years ago today" (30 Nov 2025), fetched: "On November 30, 2022, OpenAI introduced a new product to the world, innocuously describing it as 'a model called ChatGPT which interacts in a conversational way.'"

## Web search in chat (2023)
- Microsoft, "Reinventing search with a new AI-powered Microsoft Bing and Edge" (7 Feb 2023), fetched: "Bing reviews results from across the web to find and summarize the answer you're looking for." "The new Bing also cites all its sources".
- Jordi Ribas (Microsoft), "Building the New Bing" (21 Feb 2023), https://blogs.bing.com/search-quality-insights/february-2023/Building-the-New-Bing , fetched: "Prometheus leverages the power of Bing and GPT to generate a set of internal queries iteratively through a component called Bing Orchestrator"; "the model reasons over the data provided by Bing and hence it's grounded by Bing data, via the Bing Orchestrator". This is the mechanism the lesson describes: the model writes searches, a program runs them, and the results are put in front of the model.
- TechCrunch, "OpenAI connects ChatGPT to the internet" (23 Mar 2023), fetched: the browsing plugin "retrieves content from the web using the Bing search API" and shows "any websites it visited in crafting an answer, citing its sources in ChatGPT's responses." (alpha, waitlist).

## Early agent attempts (2023)
- AutoGPT's own README at tag v0.2.1 (tag commit 16 April 2023; research/sources/autogpt_README_v0.2.1.md, fetched from raw.githubusercontent.com): "This experiment aims to showcase the potential of GPT-4 but comes with some limitations: 1. Not a polished application or product, just an experiment 2. May not perform well in complex, real-world business scenarios. In fact, if it actually does, please share your results! 3. Quite expensive to run". The repository's first commits are dated 16 March 2023 (git fetch of the history).
- Lilian Weng, "LLM Powered Autonomous Agents" (23 June 2023), fetched: AutoGPT "has quite a lot of reliability issues given the natural language interface, but nevertheless a cool proof-of-concept demo." Challenges: "LLMs may make formatting errors and occasionally exhibit rebellious behavior (e.g. refuse to follow an instruction)."
- Wikipedia, "AutoGPT" (secondary, fetched), cites Cade Metz (New York Times, 10 June 2023) for "AutoGPT's tendency to get stuck in infinite loops", and Mark Sullivan (Fast Company, 13 April 2023) for "it is unaware of what it has already done". Not read at the original outlets.

## Models trained to work in the loop
- OpenAI, "Function calling and other API updates" (13 June 2023). openai.com answers 403 here; the quote was read in TechCrunch's report of the same day (fetched): "These models have been fine-tuned to both detect when a function needs to be called … and to respond with JSON that adheres to the function signature."
- Anthropic, "Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet" (6 Jan 2025), https://www.anthropic.com/engineering/swe-bench-sonnet , fetched: the scaffold is "a prompt, a Bash Tool for executing bash commands, and an Edit Tool"; "give as much control as possible to the language model itself, and keep the scaffolding minimal"; "many others contributed to training Claude 3.5 Sonnet to be excellent at agentic coding"; 49% on SWE-bench Verified.
- OpenAI, o3 and o4-mini system card (16 April 2025), PDF fetched from cdn.openai.com (text of pages 1-4 in research/sources/): "The OpenAI o-series models are trained with large-scale reinforcement learning on chains of thought." "The models use tools in their chains of thought". The launch post's sentence "we also trained both models to use tools through reinforcement learning" was read only in the search engine's copy (openai.com answers 403).

## Anthropic, "Building effective agents" (Erik Schluntz and Barry Zhang, 19 Dec 2024), fetched
- "They are typically just LLMs using tools based on environmental feedback in a loop."
- Agents need "ground truth" from the environment at each step, such as tool results or code execution.
- "the potential for compounding errors".
- Coding: "Code solutions are verifiable through automated tests; Agents can iterate on solutions using test results as feedback".

## Claude Code
- Anthropic, "Claude 3.7 Sonnet and Claude Code" (24 Feb 2025), fetched: Claude Code is "an active collaborator that can search and read code, edit files, write and run tests, commit and push code to GitHub, and use command line tools"; "a limited research preview".
- Claude Code docs, "How Claude Code works", https://code.claude.com/docs/en/how-claude-code-works , fetched 2026-09-27:
  - "Without tools, Claude can only respond with text. With tools, Claude can act"
  - "Each tool use returns information that feeds back into the loop, informing Claude's next decision."
  - "The agentic loop is powered by two components: models that reason and tools that act. Claude Code is the layer around the model that provides the tools and manages the context the model sees. This surrounding layer is what the term agentic harness refers to."
  - Context: "As you work, context fills up. Claude compacts automatically"; "It clears older tool outputs first, then summarizes the conversation if needed."
  - Permissions: "Manual: Claude asks before file edits and shell commands"; "Auto: a classifier reviews most actions in the background and blocks the risky ones instead of asking you".
- Claude Code docs, "Security", fetched: "In Manual mode, Claude Code starts with read-only permissions. When Claude Code needs to edit files, run tests, or execute commands, it asks you first".
- Latent Space podcast, "Claude Code: Anthropic's Agent in Your Terminal" (7 May 2025), https://www.latent.space/p/claude-code , Boris Cherny, fetched: "very, very early versions of Claude actually used RAG. So we, like, indexed the code base"; "the code drifts out of sync"; "eventually, we landed on just agentic search as the way to do stuff"; "Just using regular code searching, you know, glob, grep"; on how it compared: "it outperformed everything. By a lot." and "This was just vibes, so internal vibes. There's some internal benchmarks also, but mostly vibes." So the lesson says only that its developers have said searching worked better than an index built in advance.
- Boris Cherny on X (search-engine copy only; x.com answers 402): "Early versions of Claude Code used RAG + a local vector db, but we found pretty quickly that agentic search generally works better."
- Anthropic, "Effective context engineering for AI agents" (29 Sep 2025), fetched: in Claude Code, "primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time, effectively bypassing the issues of stale indexing"; "Compaction is the practice of taking a conversation nearing the context window limit, summarizing its contents, and reinitiating a new context window with the summary."
- Anthropic, "Effective harnesses for long-running agents" (Justin Young, 26 Nov 2025), fetched: "The Claude Agent SDK is a powerful, general-purpose agent harness"; compaction "enables an agent to work on a task without exhausting the context window."

## The name for the software around the model
- "harness": Claude Code docs (above) and Anthropic's Nov 2025 post. "scaffold" / "scaffolding": Anthropic's Jan 2025 SWE-bench post, and METR (both research reports). The lesson uses "harness" throughout.
