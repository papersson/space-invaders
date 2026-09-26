# LLM Agents — Canonical Sources Report

## 1. Canonical worked example

Two standard examples, serving different purposes:

- **Tool-calling primitive**: OpenAI's `get_weather(location, units)` function-calling example — the model emits `{"location":"Paris, France"}`, your code executes and returns a value. [OpenAI function calling guide](https://developers.openai.com/api/docs/guides/function-calling). This is the *far more common first example* in tutorials/docs because it needs no framework, just a JSON schema.
- **Full agent loop**: ReAct's HotpotQA example — Yao et al., *"ReAct: Synergizing Reasoning and Acting in Language Models,"* arXiv:2210.03629 (Oct 2022, ICLR 2023). Figure 1 walks the question *"Aside from the Apple Remote, what other device can control the program Apple Remote was originally designed to interact with?"* through interleaved **Thought → Action → Observation** steps using a Wikipedia search/lookup API. This is the standard **loop diagram** cited once a lesson moves past "single tool call" to "agent," and is what nearly every course/blog reuses.
- Anthropic's ["Building Effective Agents"](https://www.anthropic.com/engineering/building-effective-agents) (Dec 2024) deliberately avoids one toy example, citing real classes instead (coding agents on SWE-bench, computer use, customer support).

**Verdict**: weather/function-calling is the more common *first* example; ReAct's Thought/Action/Observation is the more common *canonical loop*.

## 2. Standard progression

Convergent across sources:

1. Plain LLM call
2. **Augmented LLM** — LLM + tools/retrieval/memory as a basic unit (Anthropic's term)
3. **Tool use / function calling** (single call, no loop)
4. **Reasoning + acting loop** — ReAct's Thought→Action→Observation, explicitly framed against two simpler baselines it improves on: *Reason-only* (chain-of-thought, hallucinates without grounding) and *Act-only* (acts without a reasoning trace, loses track of state/goal decomposition) (arXiv:2210.03629)
5. **Workflows** — predefined code paths (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer): simpler, more predictable, tried before reaching for full autonomy
6. **Autonomous agents** — LLM dynamically directs its own tool use across steps, with human checkpoints
7. Multi-agent (Berkeley CS294 course, Anthropic's orchestrator-workers pattern)

Source for 2–6: [Anthropic, "Building Effective Agents,"](https://www.anthropic.com/engineering/building-effective-agents) Dec 2024 — explicit escalation from augmented LLM → 5 workflow patterns → autonomous agents.

## 3. Standard model, definitions, terminology

- **Classical AI** (Russell & Norvig, AIMA): agent = perceives environment via sensors, acts via actuators; PEAS; rational agent. Any perceive-act loop counts (a thermostat qualifies).
- **Anthropic**: *Workflows* = "systems where LLMs and tools are orchestrated through predefined code paths." *Agents* = "systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks." ([anthropic.com/engineering/building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents))
- **OpenAI** ("A Practical Guide to Building Agents," 2024, [PDF](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)): "Agents are systems that independently accomplish tasks on your behalf... an agent uses an LLM to manage workflow execution and dynamically select tools within defined guardrails." Explicitly states simple chatbots, single-turn LLM calls, and sentiment classifiers are **not** agents.
- **LangChain**: "An Agent is a class that uses an LLM to choose a sequence of actions... In Chains, a sequence of actions is hardcoded. In Agents, a language model is used as a reasoning engine" (per LangGraph docs; exact current URL uncertain, likely `docs.langchain.com/oss/python/langgraph/workflows-agents`).
- **Terminology gap worth flagging**: classical-AI "agent" ⊃ any perceive-act system; LLM-vendor "agent" is narrower — it specifically excludes single-call/deterministic systems and requires dynamic, multi-step, LLM-directed control flow.

**What's measured**: all three major benchmarks foreground **end-to-end task success rate** as the headline metric:
- SWE-bench (arXiv:2310.06770) — resolution rate on real GitHub issues
- WebArena (arXiv:2307.13854) — functional-correctness task success
- AgentBench (arXiv:2308.03688) — 8 environments, LLM-as-agent decision-making (exact per-task metric formula: uncertain without full-paper read)

Steps/cost/human-preference are not the primary reported metric in these benchmarks (uncertain whether any reports cost internally).

## 4. Key results — exact figures

**ReAct** (arXiv:2210.03629), model **PaLM-540B**, few-shot prompted, no fine-tuning:
- HotpotQA (EM): Standard 28.7, CoT 29.4, CoT-SC 33.4, Act-only 25.7, **ReAct 27.4**, ReAct→CoT-SC 35.1. ReAct actually *trails plain CoT here* (27.4 vs 29.4) — an explicit paper caveat.
- FEVER (acc): CoT 56.3, **ReAct 60.9** — here ReAct wins.
- CoT's hallucination false-positive rate: 14% vs ReAct's 6%.
- ALFWorld: ReAct (best-of-6) **71%** vs BUTLER (best-of-8) **37%**.
- WebShop: ReAct **40.0%** vs Act-only 30.1%.
- **Where it stops holding**: ReAct is not uniformly better than CoT; best results need a hybrid switching strategy (ReAct↔CoT-SC).

**SWE-bench** (arXiv:2310.06770), 2,294 real GitHub issues, 12 Python repos: original 2023 baseline **Claude 2 solved 1.96%** (best model tested), GPT-3.5 0.17%. Scope: Python-only, patch-must-pass-tests.
- **SWE-bench Verified** (500-issue human-filtered subset, OpenAI Aug 2024): GPT-4o 33.2% (vs 16% on original set, same scaffold). ~78% of issues are <1hr of human work — **not long-horizon**.
- Anthropic-reported, same-ish benchmark family but different scaffolds/subsets over time: Claude 3.5 Sonnet (June 2024) 33.4% → (Oct 2024) 49.0% → Claude 3.7 Sonnet (Feb 2025) 63.7% (standard scaffold), 70.3% (custom high-compute scaffold). **Caveat**: subset and scaffold changed each time, so these are not strictly comparable across dates.

**Toolformer** (Schick et al., arXiv:2302.04761), GPT-J 6.7B, self-supervised, zero-shot: SVAMP 29.4 vs GPT-3-175B's 10.0; ASDiv 40.4 vs 14.0 — small tool-using model beats a much larger tool-less one on arithmetic/lookup tasks.

**WebArena** (arXiv:2307.13854): best GPT-4 agent **14.41%** success vs human **78.24%** — the standard citation for "agents lag humans badly on realistic, long web tasks."

**METR, "Measuring AI Ability to Complete Long Tasks"** (arXiv:2503.14499, Mar 2025): the 50%-success task-duration horizon has doubled roughly every ~7 months since 2019 (faster, <3 months, on a SWE-bench-Verified-based measure). Cited horizons: GPT-2 ≈2 sec; Claude 3.7 Sonnet ≈50 min; o3 ≈110 min. This is the standard modern citation for "agents fail as task horizon grows."

## 5. Standard concrete examples/transcripts

- **ReAct Fig. 1**: the Apple Remote HotpotQA question, side-by-side across Standard/CoT/Act-only/ReAct prompting, ReAct interleaving explicit Thought/Act/Obs turns with a Wikipedia search API (arXiv:2210.03629).
- **Anthropic's coding-agent note**: they report spending more effort on tool design than prompts; one concrete fix — requiring absolute filepaths in the file-edit tool — "the model used this method flawlessly" afterward ([anthropic.com/engineering/building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents)). No full published transcript.
- AutoGPT's original demo transcript: **uncertain**, not independently verified this pass.

## 6. Misconceptions and canonical corrections

- **"Agents = complex frameworks"** — Anthropic: "the most successful implementations weren't using complex frameworks... they were building with simple, composable patterns." ([source](https://www.anthropic.com/engineering/building-effective-agents))
- **Conflating workflows with agents** — corrected by Anthropic's explicit two-term split (§3 above).
- **"More autonomy is always better"** — Anthropic: autonomy brings "higher costs, and the potential for compounding errors"; recommends the simplest solution that works, escalating only when needed.
- **"Agents will replace human workers/accountability"** — Simon Willison (["I think agent may finally have a widely agreed upon definition"](https://simonw.substack.com/p/i-think-agent-may-finally-have-a)) settles on *"an LLM agent runs tools in a loop to achieve a goal,"* and separately argues agents lack the accountability that makes a human a genuine "agent" (citing a 1979 IBM slide: "A computer can never be held accountable").
- **"Agents need bespoke long-term memory"** — Willison: conversation history within the loop is usually sufficient; don't over-engineer memory before it's needed.

## 7. For a short lesson: essential / extra / omit

**Essential**:
- The loop itself: LLM proposes an action → code executes it → result fed back → repeat until done (the ReAct Thought/Action/Observation shape).
- The workflow-vs-agent distinction (Anthropic) — this is the single highest-leverage conceptual clarification for engineers who'll otherwise think "agent" means "chatbot with extra steps."
- Why it fails: compounding error over steps, and the benchmark numbers showing large agent-vs-human gaps on realistic tasks (WebArena 14% vs 78%; METR's task-horizon curve).

**Common extra** (include only if time permits): multi-agent orchestration patterns, memory architectures (vector DBs), the AutoGPT self-prompting loop as a historical/cautionary example.

**Leave out**: AIMA-level PEAS/rational-agent formalism (adds classical-AI baggage without payoff for this audience); benchmark internals (AgentBench's 8 environments, exact metric formulas); framework-specific APIs beyond one worked mechanism (don't survey LangChain + AutoGPT + Assistants API + Agents SDK all in one lesson — pick one).

## 8. Real systems, frameworks, APIs — exact mechanism

- **OpenAI function/tool calling**: model returns a structured `tool_calls` object matching a JSON schema you supplied; your backend executes it, not the model. ([docs](https://developers.openai.com/api/docs/guides/function-calling))
- **OpenAI Assistants API → Responses API/Agents SDK**: Assistants API deprecated Aug 2025, sunset Aug 2026; superseded by the Responses API (Mar 2025) + Agents SDK with built-in tools (web search, file search, computer use) and tracing.
- **Anthropic tool use**: model emits a `tool_use` content block, `stop_reason: "tool_use"`; you execute client-side tools and return a `tool_result` block next turn; some tools (web search, code execution) run server-side on Anthropic's infra. ([docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview))
- **Claude computer use** (Oct 2024): loop of screenshot → model returns pixel-coordinate click/type actions → app executes → new screenshot returned. ([Anthropic announcement](https://www.anthropic.com/news/3-5-models-and-computer-use); [Willison's writeup](https://simonwillison.net/2024/Oct/22/computer-use/))
- **LangChain/LangGraph**: the older `AgentExecutor` (hardcoded loop) is deprecated in favor of LangGraph's explicit node/edge state-machine graph, giving branching, persistence, and human-in-the-loop.
- **AutoGPT (2023)**: loop of goal → task planning → tool selection → LLM call → action → self-critique → repeat, with a vector-DB memory and task queue (widely repeated secondary-source description; original repo not independently re-verified here).
- **ReAct**: a **prompting** technique (few-shot, frozen weights), not a fine-tuned model or product — worth stressing since it's often confused with a "framework."

## 9. Commonly overstated/subtly wrong claims

- **The "0.95^n compounding-error" arithmetic** (e.g., 95%/step → ~60% success at 10 steps) appears widely in **industry blogs**, not in a vendor-canonical or peer-reviewed source. Treat the *concept* (errors compound over steps) as canonical (Anthropic names the risk); treat the specific exponent-style numbers as illustrative commentary, not a measured constant.
- **Chain-of-thought reflects true reasoning** — Anthropic's own research ("[Reasoning models don't always say what they think](https://www.anthropic.com/research/reasoning-models-dont-say-think)") found CoT faithfulness on hint-injection tests often below 20%, sometimes ~1%, and that larger/more capable models can be *less* faithful, not more.
- **Autonomy readiness overstated** — Anthropic's agent-autonomy research reports real Claude Code users auto-approve only ~20–40% of actions even among experienced users, undercutting "agents are already fully autonomous in practice" narratives.
- **Benchmark success transfers directly to production** — a recurring point in Willison's commentary: benchmarks don't model real-world flakiness (auth failures, rate limits, ambiguous UI state) that agents hit in deployment.

## 10. Animation vs. hands-on vs. reading

- **Narrated animation**: the loop itself (Thought→Action→Observation cycling, tool_use/tool_result round-trip) — this is inherently a *process over time* and reads far better animated than as static prose; also good for the workflow-vs-agent distinction (predefined path vs. dynamically-chosen path) shown as diverging diagrams.
- **Hands-on (run code)**: give the audience a single tool-calling example to run themselves (e.g., OpenAI/Anthropic weather- or file-edit-tool example) — engineers in this audience learn the request/response shape fastest by seeing the actual JSON. A tiny ReAct-style loop (10–20 lines) reinforces that "agent" is just code around an LLM call, not magic.
- **Reading**: the exact benchmark numbers and caveats (§4) are better read/paused-on than narrated — precision and caveats (subset changed, scaffold changed) get lost in voiceover pacing; link out to the papers/posts rather than reciting all figures aloud.
