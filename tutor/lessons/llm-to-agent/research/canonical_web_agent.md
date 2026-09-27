# From LLM to Agent — Research Report for a Narrated Explainer

*Sources actually read in full (fetched primary documents): Anthropic, ["Building Effective AI Agents"](https://www.anthropic.com/research/building-effective-agents) (Dec 19, 2024); Lilian Weng, ["LLM Powered Autonomous Agents"](https://lilianweng.github.io/posts/2023-06-23-agent/) (Jun 23, 2023); Anthropic, ["Claude Code Best Practices"](https://code.claude.com/docs/en/best-practices) (current docs); Anthropic, ["Claude SWE-bench Performance"](https://www.anthropic.com/engineering/swe-bench-sonnet) (Jan 6, 2025); Latent Space, ["Claude Code: Anthropic's Agent in Your Terminal"](https://www.latent.space/p/claude-code) (interview w/ Boris Cherny, May 7, 2025). All other facts below were checked via search snippets from the cited outlets/arXiv pages, not full fetches; I flag anything I could not directly verify.

---

## 1. Canonical worked example

There are two competing standard examples, used at different levels:

- **"Predict the next word" example** (e.g. "The cat sat on the ___") — the canonical way every non-specialist explainer (Karpathy's ["Intro to Large Language Models"](https://www.youtube.com/watch?v=zjkBMFhNj_g), Nov 23 2023; 3Blue1Brown's ["Large Language Models explained briefly"](https://www.3blue1brown.com/lessons/mini-llm/), Nov 20 2024) introduces what an LLM *is*, before agency is discussed at all.
- **"Debug a failing test" / "fix a GitHub issue" example** — the canonical way the *agent* step is introduced. This is the example in SWE-bench (Yao/Jimenez et al., ["SWE-bench: Can Language Models Resolve Real-World GitHub Issues?"](https://arxiv.org/abs/2310.06770), Oct 2023), in Cognition's Devin launch (["Introducing Devin"](https://cognition.com/blog/introducing-devin), Mar 12 2024), and in Anthropic's own Claude Code documentation, which frames the tool around exactly this loop: *"Claude Code can read your files, run commands, make changes, and autonomously work through problems"* ([Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)).

**More common:** the fix-a-bug/resolve-a-GitHub-issue example is the dominant one for teaching "LLM → agent," because it is concrete, verifiable (tests pass/fail), and is literally the framing of the lesson prompt you gave me. It is also the example used by essentially every coding-agent vendor doc (Anthropic, Cognition, OpenAI's Codex docs).

## 2. Standard progression across canonical sources

1. **LLM as next-token predictor** (Karpathy 2023; 3Blue1Brown 2024) — no agency yet.
2. **LLM + single tool call**, e.g. a calculator or search API — Toolformer (Schick et al., [arXiv:2302.04761](https://arxiv.org/abs/2302.04761), Feb 2023) and OpenAI's [function calling](https://openai.com/index/function-calling-and-other-api-updates/) (Jun 13, 2023) sit here: the model outputs structured intent, code executes it, result is fed back in text.
3. **Interleaved reasoning + acting in a loop** — ReAct (Yao et al., [arXiv:2210.03629](https://arxiv.org/abs/2210.03629), Oct 2022, ICLR 2023): "Thought → Action → Observation" repeated. This is the standard template almost every later agent framework (LangChain's `AgentExecutor`, METR's evaluation "scaffolds") explicitly cites as its ancestor.
4. **Full autonomous loop with planning + memory** — Lilian Weng's ["LLM Powered Autonomous Agents"](https://lilianweng.github.io/posts/2023-06-23-agent/) (Jun 2023) is the standard synthesis: LLM-as-controller + Planning + Memory + Tool Use, illustrated with AutoGPT/BabyAGI/GPT-Engineer as (imperfect) worked proofs of concept.
5. **Production framing: workflow vs. agent** — Anthropic's ["Building Effective Agents"](https://www.anthropic.com/research/building-effective-agents) (Dec 19, 2024) is the standard vendor-level document that says: start with a plain "augmented LLM," compose fixed pipelines ("workflows") first, and reserve the label "agent" for the harder case where the model itself decides the next step. OpenAI's ["A Practical Guide to Building Agents"](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) (Apr 17, 2025) mirrors this same simple→complex progression.

So the standard order is: predict text → call one tool → reason/act loop → planning+memory agent → "only use an agent when a workflow won't do."

## 3. Standard definitions and terminology

- **LLM**: a model trained to predict the next token of text given prior tokens; it has no persistent state and does not act on its own — this is the definition used throughout Karpathy's talk and both Weng's and Anthropic's posts.
- **Agent**, per Anthropic: *"systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks"* ([Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)).
- **Agent**, per OpenAI: *"systems that independently accomplish tasks on your behalf"*, using an LLM "to manage workflow execution and dynamically select tools within defined guardrails" — and explicitly *not* a single-turn LLM call, a chatbot, or a classifier ([A Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)).
- **Workflow** (Anthropic): "LLMs and tools orchestrated through predefined code paths" — the opposite of an agent; the two vendors' definitions agree in substance even though the exact wording differs.
- **The software around the model**: no single agreed term.
  - Anthropic/OpenAI docs mostly just say "agent" for the whole system (model + tools + loop).
  - **METR** and the alignment-evaluation community call it a **"scaffold"** or **"agent scaffold"** — e.g. METR's Modular and Triframe scaffolds ([metr.org](https://metr.org/measuring-autonomous-ai-capabilities/)), a term borrowed informally from "scaffolding" in construction — the harness is temporary infrastructure around the model.
  - Practitioners also use **"harness"** informally (common in Anthropic/OpenAI engineering discussion, e.g. Boris Cherny in the Latent Space interview).
  - LangChain's docs call the loop-runner an **`AgentExecutor`**.
  So: *agent* = model + tools + loop as an interacting whole; *scaffold/harness* = the surrounding code specifically, as distinct from the model itself. This is a genuine terminology split worth flagging in the video as "people use different words for the same box."

## 4. Key results, exact figures, assumptions, and limits

- **SWE-bench** (Jimenez et al., [arXiv:2310.06770](https://arxiv.org/abs/2310.06770), Oct 2023): 2,294 real GitHub issue/PR pairs from 12 Python repos. Ground truth = whether the model's patch makes the repo's real hidden test suite pass. Best baseline (Claude 2 + RAG) at launch: **1.96%** resolved. This number is *specific to that RAG-retrieval baseline*, not to agentic tool use — it stops holding as soon as any real tool-use loop is added.
- **Devin** (Cognition, Mar 12, 2024): claimed **13.86%** resolved unassisted vs. the then-existing 4.80% "assisted" state of the art — a large jump attributed to giving the model a persistent sandboxed dev environment, not just one-shot patch generation ([Cognition blog](https://cognition.com/blog/introducing-devin)).
- **Claude 3.5 Sonnet (Oct 2024)**: **49%** on SWE-bench Verified (a human-filtered 500-task subset), vs. 45% prior SOTA, achieved with — per Anthropic's own account — **only two tools**, a bash tool and a file-edit tool, and a deliberately *minimal* scaffold: *"give as much control as possible to the language model itself, and keep the scaffolding minimal"* ([anthropic.com/engineering/swe-bench-sonnet](https://www.anthropic.com/engineering/swe-bench-sonnet), Jan 6 2025). This is the standard citation for "simple tools + smart model beats complex orchestration."
- **Reliability over many steps**: the canonical explanation, given consistently by Anthropic (Building Effective Agents), METR, and Claude Code docs, is that *errors compound multiplicatively across steps* — if each step is independently correct with probability p, an n-step task succeeds with roughly p^n — so the standard fixes are (a) give the agent an external, checkable signal (tests, exit codes, screenshots) so it can self-correct rather than accumulate silent error, and (b) keep context/scaffolding simple so the model isn't fighting its own harness. METR frames this quantitatively as **"time horizon"**: the length of task (measured in estimated human-expert time) a model can complete autonomously at a fixed success rate, which is their standard way of expressing "reliability degrades with task length" ([METR](https://metr.org/measuring-autonomous-ai-capabilities/)). I could not independently verify a specific published METR time-horizon number in this session and flag any exact percentage/hour figure as **uncertain** without a direct fetch of METR's dated report.

## 5. Standard concrete examples in canonical sources

- **Next-token example**: Karpathy and 3Blue1Brown both use short everyday sentences with a visible probability distribution over next words as the standard illustration of "an LLM is a next-word predictor," explicitly with no agency implied.
- **ReAct transcripts** (Yao et al. 2022): interleaved `Thought: ... / Action: Search[...] / Observation: ...` traces on HotpotQA (multi-hop QA over Wikipedia) and ALFWorld (a text-adventure "go to the fridge and get an apple" environment) — this exact transcript format is the one nearly every later agent tutorial (LangChain docs included) reuses.
- **Weng's case studies**: AutoGPT/BabyAGI/GPT-Engineer as "proof-of-concept" agents that plan, use tools, and reflect, explicitly flagged in her post as impressive demos with poor real-world reliability.
- **Anthropic's tool examples**: the bash tool and edit tool (view/create/str_replace/insert/undo_edit) from the SWE-bench Sonnet post are the standard concrete "what a coding agent's tools actually look like" example.

## 6. Misconceptions and how canon corrects them

- *"ChatGPT / the model itself does things now"* — canon (Anthropic, OpenAI, Weng) is explicit that the model still only ever outputs text; "doing things" is entirely the surrounding scaffold parsing that text as a tool call and executing it, then feeding a text observation back in. The video's core job is to make this loop visible.
- *"More autonomy/more tools = better agent"* — directly contradicted by Anthropic's own result: the highest SWE-bench score came from **fewer**, better-designed tools and a **thinner** scaffold, not more ([SWE-bench Sonnet post](https://www.anthropic.com/engineering/swe-bench-sonnet)); Anthropic's Building Effective Agents post opens by warning against reaching for "agent" architectures before simpler workflows are tried.
- *"Agents are a 2023-in some Model breakthrough"* — actually the mechanism (interleaved reasoning+action) predates the AutoGPT hype wave; ReAct (Oct 2022) and even OpenAI's WebGPT (Dec 2021, [arXiv:2112.09332](https://arxiv.org/abs/2112.09332)) already had models issuing search actions and reading results. What changed by 2023–2024 was *model reliability*, not the invention of the loop.
- *"The model retrieves the right code by understanding the whole repo semantically"* — canon (Claude Code) explicitly rejects this; see section 8.
- *"Hallucination is a bug that agents fix"* — canon treats hallucination as a base property of next-token prediction (Karpathy's talk) that agentic tool use *mitigates* (by grounding claims in tool output) but does not eliminate.

## 7. For a short lesson: essential / extra / cut

- **Essential**: (a) LLM = text-in, text-out, next-token predictor, no hands; (b) the loop — model proposes an action in text → scaffold executes it (read file / run test) → result fed back as text → repeat; (c) the loop stops when a check (tests passing) says so, not when the model "feels done" — this is literally how Claude Code's own docs describe the difference between a chatbot and an agent (["Give Claude a way to verify its work"](https://code.claude.com/docs/en/best-practices)).
- **Common extra** (include if time allows): the workflow-vs-agent distinction (Anthropic), and the "fewer tools, simpler scaffold" result — great because it's counterintuitive and citable with an exact number (49%).
- **Leave out**: ReAct/Toolformer paper mechanics, memory architectures (vector stores), multi-agent orchestration, benchmark methodology details (contamination, "Verified" subset curation), and the terminology dispute (agent vs. scaffold vs. harness) — interesting to specialists, not needed for the lesson's stated goal.

## 8. Real systems and mechanisms, with primary sources

- **WebGPT** (OpenAI, Dec 2021): search-and-cite loop over a text-based browser, trained via human feedback — earliest well-known "LLM + live tool" system ([arXiv:2112.09332](https://arxiv.org/abs/2112.09332)).
- **Bing Chat** (Microsoft, launched Feb 7, 2023): first widely known consumer chat product with live web search built in ([Microsoft blog](https://blogs.microsoft.com/blog/2023/02/07/reinventing-search-with-a-new-ai-powered-microsoft-bing-and-edge-your-copilot-for-the-web/); [TechCrunch](https://techcrunch.com/2023/02/07/microsoft-launches-the-new-bing-with-chatgpt-built-in/)).
- **ChatGPT plugins incl. Browse** (OpenAI, Mar 23, 2023): first-party browsing plugin using Bing's API, alpha rollout to waitlisted Plus users ([TechCrunch](https://techcrunch.com/2023/03/23/openai-connects-chatgpt-to-the-internet/)).
- **AutoGPT** (Toran Bruce Richards, released Mar 2023) and **BabyAGI** (Yohei Nakajima, 2023): open-source, viral, largely-unreliable autonomous-loop demos — canonically cited (Weng 2023) as proof-of-concept rather than production-grade.
- **Devin** (Cognition, Mar 12, 2024): first product marketed as "AI software engineer"; 13.86% SWE-bench unassisted ([Cognition](https://cognition.com/blog/introducing-devin)).
- **Claude Code** (Anthropic): announced as a research preview **Feb 24, 2025** with Claude 3.7 Sonnet; general availability **May 22, 2025** (per search-aggregated sources; I did not fetch Anthropic's original launch post directly this session, so treat the exact GA date as reasonably but not fully confirmed).

**How Claude Code finds relevant code, specifically:** Anthropic's own engineers state they *tried* a RAG pipeline (embeddings + vector database over the codebase) first, then replaced it with **agentic search**: the model uses ordinary developer tools — `grep`, `glob`, directory listing, file reads — iteratively, deciding for itself what to look at next, the same way a human engineer would explore an unfamiliar repo. In Boris Cherny's words on Latent Space (May 7, 2025): *"It outperformed everything. By a lot,"* and RAG's indexing step was rejected because *"the code drifts out of sync... it's just a lot of liability,"* whereas *"agentic search just sidesteps all of that... at the cost of latency and tokens"* ([Latent Space interview](https://www.latent.space/p/claude-code)). The current official docs describe the same idea generally (["explore, plan, code, commit"](https://code.claude.com/docs/en/best-practices)) without mentioning embeddings at all — retrieval is just another agentic action, not a separate subsystem. This is a good, citable, and slightly counterintuitive detail for the video: the state-of-the-art coding agent finds code the low-tech way, on purpose.

## 9. History, exact dates, primary sources

| Date | Event | Source |
|---|---|---|
| Dec 2021 | WebGPT: first well-known LLM+browsing system | [arXiv:2112.09332](https://arxiv.org/abs/2112.09332) |
| Nov 30, 2022 | ChatGPT launched (free research preview) | [OpenAI/history.com](https://www.history.com/this-day-in-history/november-30/chatgpt-released-openai) |
| Oct 2022 (paper), ICLR 2023 | ReAct paper — canonical reasoning+acting loop | [arXiv:2210.03629](https://arxiv.org/abs/2210.03629) |
| Feb 7, 2023 | Bing Chat: first widely known chat assistant with integrated live web search | [Microsoft](https://blogs.microsoft.com/blog/2023/02/07/reinventing-search-with-a-new-ai-powered-microsoft-bing-and-edge-your-copilot-for-the-web/) |
| Feb 9, 2023 | Toolformer paper | [arXiv:2302.04761](https://arxiv.org/abs/2302.04761) |
| Mar 2023 | AutoGPT released; BabyAGI shared — first widely known ("viral") autonomous LLM agent attempts, unreliable in practice | search-aggregated (Fast Company, IBM) |
| Mar 23, 2023 | ChatGPT plugins incl. browsing, alpha | [TechCrunch](https://techcrunch.com/2023/03/23/openai-connects-chatgpt-to-the-internet/) |
| Jun 13, 2023 | OpenAI function calling API | [OpenAI](https://openai.com/index/function-calling-and-other-api-updates/) |
| Jun 23, 2023 | Lilian Weng's "LLM Powered Autonomous Agents" — standard synthesis essay | [lilianweng.github.io](https://lilianweng.github.io/posts/2023-06-23-agent/) |
| Oct 2023 | SWE-bench paper published | [arXiv:2310.06770](https://arxiv.org/abs/2310.06770) |
| Nov 23, 2023 | Karpathy's "Intro to Large Language Models" talk | search-aggregated |
| Mar 12, 2024 | Devin announced by Cognition | [Cognition blog](https://cognition.com/blog/introducing-devin) |
| Dec 19, 2024 | Anthropic "Building Effective Agents" | [anthropic.com](https://www.anthropic.com/research/building-effective-agents) |
| Jan 6, 2025 | Anthropic SWE-bench Sonnet post (minimal-scaffold result) | [anthropic.com/engineering](https://www.anthropic.com/engineering/swe-bench-sonnet) |
| Feb 24, 2025 | Claude Code research preview | search-aggregated, **uncertain, not directly fetched from Anthropic** |
| Apr 17, 2025 | OpenAI "A Practical Guide to Building Agents" | [OpenAI PDF](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) |
| May 7, 2025 | Latent Space interview w/ Boris Cherny on Claude Code's agentic search design | [latent.space](https://www.latent.space/p/claude-code) |
| May 22, 2025 | Claude Code general availability | search-aggregated, **uncertain, not directly fetched from Anthropic** |

**What changed between AutoGPT (2023) and working coding agents (2024–25), per the people who built them:** Anthropic's own account attributes the jump largely to (1) better base-model reliability at multi-step tool use, and (2) *deliberately simpler* scaffolding rather than more elaborate planning/memory architecture — the opposite of AutoGPT's "give it lots of autonomous machinery" approach ([SWE-bench Sonnet post](https://www.anthropic.com/engineering/swe-bench-sonnet); [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)).

## 10. Overstated or subtly wrong claims

- "Agents are autonomous" is often overstated: canonical docs (Anthropic, OpenAI) both stress agents run *within guardrails a human sets* (allowed tools, permission prompts, budgets) — not unbounded autonomy.
- "SWE-bench percentages measure real-world coding ability": the benchmark measures resolving *already-triaged, already-reproducible* GitHub issues in popular, well-tested Python repos — not general software engineering, and scores are known to be sensitive to contamination and to the specific "Verified"/filtered subset used.
- "AutoGPT/BabyAGI were the first agents": the reasoning-acting loop was already published (ReAct, WebGPT) before these viral open-source projects; what AutoGPT/BabyAGI did was popularize the *idea*, not invent the mechanism, and they are cited by Weng specifically as unreliable proofs of concept, not working systems.
- "Claude Code understands your whole codebase": per Anthropic's own engineers, it deliberately does *not* build a semantic understanding of the whole repo up front; it re-explores relevant parts fresh each time, on purpose.
- "More tools/more autonomy makes agents better": Anthropic's highest-scoring SWE-bench configuration used only two tools — this is the standard counter-citation to that claim.

## 11. Animation vs. interactive vs. reading

- **Best as narrated animation**: the core mental model — token-by-token text prediction; the "propose action → execute → observe → repeat" loop drawn as a literal loop diagram; the workflow-vs-agent distinction as two flowchart shapes. These are inherently visual/sequential ideas that a static read or a hands-on exercise conveys less clearly than watching state change over time.
- **Best learned by doing**: the *feel* of an agent loop — e.g. having the viewer (or a companion interactive demo) watch Claude Code or a similar tool actually read a file, run a failing test, and fix it, because the "it stops when the test passes, not when it feels done" idea (explicit in [Claude Code's docs](https://code.claude.com/docs/en/best-practices)) is best internalized by seeing a real pass/fail signal drive real iteration, not by being told about it.
- **Best as reading/reference** (not for the video itself, but worth linking in a description): the original ReAct paper transcript format and Anthropic's Building Effective Agents post, for viewers who want the "textbook" version after the narrative lands.
