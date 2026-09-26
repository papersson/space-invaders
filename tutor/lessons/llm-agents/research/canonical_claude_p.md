Note: WebSearch access was denied in this session, so I'm answering from training knowledge rather than live-verified sources. I've flagged every figure I'm not fully confident of — please spot-check those against the primary source before quoting them in narration.

## 1. Canonical worked example

Two competing ones, both still in circulation:

- **ReAct's Wikipedia-search QA loop** — Yao et al., *"ReAct: Synergizing Reasoning and Acting in Language Models,"* ICLR 2023 (arXiv 2022). The worked example is a multi-hop trivia question answered via an alternating `Thought → Action: Search[x]/Lookup[x] → Observation` loop against a Wikipedia API. It's the standard *academic* worked example because it's the smallest possible instance of the reasoning+acting+observation loop — one tool, plain text, no scaffolding — and it's the one reproduced in Lilian Weng's *"LLM Powered Autonomous Agents"* (June 2023, widely treated as the field's reference essay) and in most course notes and LangChain's early "ReAct agent" docs.
- **The tool-calling customer-support/coding-agent example** — used in Anthropic's *"Building Effective Agents"* (Schluntz & Zhang, Dec 2024) and OpenAI's function-calling / Assistants docs. This is now the more common worked example for a *software-engineer* audience specifically, because it maps directly onto things engineers already build (an API-calling loop that looks up an order, or opens/fixes a GitHub issue).

**For your audience (working SWE), the second is more common in the material they'd actually read** (vendor docs), but the first is the one you'll see cited as "the" canonical example if you go back to papers/courses. Worth naming both and saying so on screen.

## 2. Standard progression

The order used almost universally, from Weng (2023), Anthropic's agent docs, and most course treatments:

1. **Plain LLM call** — stateless text-in/text-out, no loop.
2. **Chain-of-thought prompting** — Wei et al., *"Chain-of-Thought Prompting Elicits Reasoning in Large Language Models,"* NeurIPS 2022. Reasoning, but no acting on the world.
3. **Tool use bolted on** — Toolformer, Schick et al. 2023 (arXiv), model learns *when* to call an API (calculator, search, calendar) via self-supervised examples; also Schick's contemporaries MRKL and TALM (both cited in Weng's post). Acting, but typically single-shot, not a loop.
4. **ReAct: reasoning + acting + observing, in a loop** — the "full" agent loop appears here for the first time as a named, benchmarked idea (2022/2023).
5. **Add memory/self-correction across attempts** — Reflexion, Shinn et al., NeurIPS 2023: the agent critiques its own failed trajectory in language and retries, without weight updates.
6. **Add planning/task decomposition and long-horizon autonomy** — AutoGPT and BabyAGI (2023, GitHub projects, not peer-reviewed but treated as canonical *cautionary* examples in every retrospective), then Voyager (Wang et al. 2023, embodied Minecraft agent with a growing skill library) as the more rigorous version of the same idea.
7. **Standardize the interface** — OpenAI function calling (2023) → Assistants API (Nov 2023) → Anthropic tool use → Model Context Protocol, Anthropic, Nov 2024 (a protocol standardizing how agents discover/call tools and resources across vendors).
8. **Evaluate it properly** — benchmarks: AgentBench, WebArena, GAIA, SWE-bench, METR's long-task-horizon work (all 2023–2025).

The "simpler version before the full version" pattern is consistent: every source shows *reasoning-only* (CoT), then *acting-only* (plain tool call), before showing the interleaved loop as the payoff.

## 3. Standard model, definitions, terminology

- **Classical AI definition** (Russell & Norvig, *Artificial Intelligence: A Modern Approach*): an agent is anything that perceives its environment through sensors and acts upon it through actuators; a *rational agent* selects actions to maximize a performance measure given its percept history (the PEAS framework: Performance, Environment, Actuators, Sensors). This predates LLMs by decades and is not about language models at all.
- **LLM-agent usage** (Anthropic's *Building Effective Agents*, 2024; also Weng 2023): the field has converged on a looser, capability-based definition. Anthropic explicitly distinguishes:
  - **Workflows** — LLM calls orchestrated through predefined code paths.
  - **Agents** — systems where the LLM dynamically directs its own process and tool use, maintaining control over how it accomplishes a task.
  Anthropic frames "agentic" as a **spectrum**, not a binary — this is the terminology point worth putting on screen, since it directly resolves the audience's likely confusion about "is this thing I built an agent or not."
- **What's measured** in evaluations: task success/resolution rate on a held-out benchmark (SWE-bench: % of GitHub issues resolved; WebArena: % of browser tasks completed end-to-end), sometimes with cost/step-count as a secondary axis, and increasingly **time-horizon** — METR's 2025 paper measures the length of a task (in human-expert-minutes) a model can complete with 50% reliability, not just pass/fail on fixed tasks.
- **Terminology divergence**: classical AI calls the perceive-act cycle "the agent function"; the LLM-agent world calls the same thing "the agent loop" and rarely invokes rationality/performance-measure language at all. Simon Willison's blog (2023, *"Agents" essays*) is the most-cited honest acknowledgment that the industry term "agent" is used inconsistently across vendors — worth citing directly if you want a beat on "the term itself is contested."

## 4. Key results, exact figures, and where they break

Flag: several of these numbers I recall approximately from training and could not re-verify via search this session — treat as "check before narrating as precise."

- **ReAct (2023)**: on ALFWorld (embodied task completion), ReAct substantially outperformed imitation-learning and act-only baselines (I recall success rates in the ~70% range for ReAct vs. ~30-45% for act-only baselines — **verify exact numbers before quoting**). On HotpotQA/QA tasks, the paper's headline point is qualitative as much as quantitative: ReAct reduces hallucination/error propagation relative to chain-of-thought-alone, because it grounds reasoning in real tool observations. Assumption: tools are reliable and cheap to call; breaks down when the tool itself is noisy or the action space is large/ambiguous.
- **Toolformer (2023)**: a 6.7B-parameter model taught to call APIs zero-shot **outperforms a much larger GPT-3 (175B)** on several downstream tasks (math word problems, QA, translation) without task-specific fine-tuning. Holds only for the narrow set of tools it was trained to call; doesn't generalize to arbitrary new tools without retraining.
- **Reflexion (2023)**: self-reflection loop improves pass rates on coding (HumanEval) and decision-making benchmarks over a single-shot baseline. Assumption: there must be a verifiable success/failure signal to reflect on (e.g., unit tests) — this is the key limiting condition; it doesn't help when success can't be checked.
- **SWE-bench** (Jimenez et al. 2023, and the human-filtered **SWE-bench Verified**, 2024): early agent scaffolds resolved single-digit to low-teens percent of real GitHub issues; state-of-the-art has moved substantially higher through 2024–2025 with better scaffolding and models. **I do not have a verified current percentage to cite — this number moves quickly and is exactly the kind of figure to look up fresh rather than narrate from memory.**
- **GAIA benchmark** (Mialon et al. 2023): designed so humans score ~90%+ while contemporary LLM-only baselines scored far lower, especially on the hardest tier requiring multi-step tool use — the point of the benchmark is precisely that "easy for a human, hard for an agent" gap.
- **METR (2025), "Measuring AI Ability to Complete Long Tasks"**: the length of task (in human-time-to-complete) that a frontier model can complete at 50% reliability has been **doubling roughly every ~7 months** since about 2019. This is the standard citation for "agents are improving on a predictable exponential, but absolute horizon is still short." Assumption: extrapolation is empirical curve-fitting, not a guaranteed law — the paper itself flags this.

## 5. Standard concrete examples/transcripts as they appear canonically

- ReAct's own paper transcript: `Question: ... Thought 1: I need to search... Action 1: Search[X] Observation 1: ... Thought 2: ... Action 2: Search[Y] ... Action n: Finish[answer]` — this exact Thought/Action/Observation transcript format is reused verbatim in Weng's post, most course slides, and LangChain's legacy ReAct-agent docs.
- AutoGPT's public demo transcripts (early 2023) of open-ended goals ("research and summarize X, write a report") looping into repeated, non-terminating sub-goals — cited universally as the go-to *failure-mode* example (goal drift, hallucinated "task complete" markers, cost blowup) rather than a success example.
- Anthropic's and OpenAI's docs use a **weather-lookup / order-status-lookup function-calling transcript** as the minimal "hello world" of tool calling before scaling up to multi-step agents.
- Voyager's skill-library transcripts (Minecraft) — cited as the standard example of an agent that writes and stores reusable code as a form of long-term memory.

## 6. Misconceptions and how the canonical treatment corrects them

- **"An agent is just a chatbot with more steps."** Corrected by the workflow-vs-agent distinction (Anthropic 2024): a fixed multi-step *pipeline* is a workflow, not an agent — the defining feature is the LLM controlling its own next action based on live feedback, not a human-authored fixed sequence.
- **"More autonomy is strictly better."** Anthropic and the AutoGPT retrospective both explicitly argue the opposite: added autonomy trades off reliability and cost, and the standard advice is to use the simplest structure (single call, then workflow) that solves the task, escalating to a full agent only when the task's open-endedness requires it.
- **"Agents fail because models aren't smart enough."** The canonical framing (Weng 2023, ReAct paper, Reflexion paper) attributes most failures instead to compounding error over long trajectories, unreliable self-assessment of success, and context/memory limits — i.e., a systems problem, not purely a raw-capability problem. METR's horizon framing reinforces this: it's not "can it reason," it's "how long a task can it stay coherent and correct on."
- **"Tool use = agent."** Toolformer/function-calling is necessary but not sufficient; the loop (deciding *whether* and *when* to act again based on an observation) is what the field calls "agentic," not the mere existence of a tool call.
- **"There's one settled definition of agent."** There isn't — worth explicitly telling the audience this is genuinely contested terminology (Willison 2023), rather than implying they missed a standard definition somewhere.

## 7. For a short lesson: essential / common-extra / cut

- **Essential**: the agent loop itself (LLM → action/tool call → observation → back to LLM); the workflow-vs-agent distinction (Anthropic 2024); one concrete transcript (ReAct-style or tool-calling-style); why it fails (compounding error, no ground-truth self-check, context limits) rather than just "why it's cool."
- **Common extra** (include if time allows, cut first if not): memory taxonomy (short-term/context vs. long-term/vector store), Reflexion-style self-critique, benchmark numbers beyond one headline figure.
- **Leave out for this audience/length**: the classical Russell & Norvig PEAS apparatus in full (a one-line contrast is enough), multi-agent orchestration frameworks, MCP protocol internals, and any deep dive into RL/fine-tuning-based agent training (out of scope for "what an agent is and why it works/fails").

## 8. Real systems/frameworks canonically cited, with mechanism

- **OpenAI function calling / Assistants API** (2023–2024): model emits a structured JSON call matching a developer-provided schema; the host code executes it and feeds the result back into context.
- **Anthropic tool use API + Model Context Protocol** (2024): same function-calling mechanism, plus MCP standardizes tool/resource discovery so one client can talk to many tool servers.
- **LangChain `AgentExecutor` / ReAct agent** (docs, 2023–): implements the literal Thought/Action/Observation string-parsing loop from the ReAct paper as a reusable abstraction.
- **AutoGPT / BabyAGI** (2023): maintain an explicit task list/queue in a prompt or vector store, and re-prompt the LLM to generate, prioritize, and re-insert sub-tasks — the mechanism that produces their characteristic infinite-loop failure mode.
- **Anthropic computer use** (Oct 2024, beta): agent takes screenshots, emits mouse/keyboard actions, evaluated against OSWorld-style benchmarks — mechanism is vision-grounded action rather than API calls.
- **Voyager** (2023): mechanism is code-as-action — the agent writes JavaScript functions against a fixed Minecraft API and stores successful ones in a persistent skill library.

## 9. Claims commonly overstated or subtly wrong

- **"Agents are basically autonomous now."** METR's own horizon numbers (doubling every ~7 months from a low absolute base) argue against near-term full autonomy on long, open-ended tasks — the trend is real but the absolute horizon today is still short.
- **"Benchmark X score = real-world reliability."** SWE-bench/GAIA/WebArena scores are on curated, verifiable tasks; canonical treatments (including the benchmark papers themselves) caution against reading them as general real-world success rates, because held-out benchmarks select for verifiable, bounded tasks unlike messy production environments.
- **"ReAct/Reflexion solved hallucination."** They *reduce* it by grounding steps in tool observations and by adding self-critique, not eliminate it — both papers report residual failure rates, not zero.
- **"Bigger model = better agent."** Toolformer's own headline result (a small model with tools beats a much larger model without them) is often cited to make the opposite point: scaffolding/tool access can matter more than raw parameter count for agentic tasks.
- **"An agent needs an LLM per action."** Many practical frameworks amortize cost by having one LLM call plan several actions or by caching/reusing sub-plans — the "one model call per atomic action" mental model oversimplifies actual implementations.

## 10. Animation vs. hands-on vs. reading

- **Narrated animation** (best fit for your medium): the agent loop itself (Thought→Action→Observation, and where control returns to the LLM) — this is inherently a *process over time* that's hard to grasp from a static diagram, and is exactly what ReAct-style transcripts are trying to convey. Also good for animating: the workflow-vs-agent spectrum, and a "compounding error over N steps" visualization (why an 90%-per-step-reliable agent still fails often over 10+ steps — a probability decay curve is a strong, concrete visual and directly explains "why it fails").
- **Hands-on/interactive** (better than narration, if you can afford a follow-up exercise): actually wiring a minimal tool-calling loop (e.g., a 20-line Python loop calling an LLM API with one tool) — the "aha" of realizing the loop is just a while-loop with string/JSON parsing is best learned by writing it, not watching it.
- **Reading** (better than either video format): the exact benchmark tables/figures and their caveats (SWE-bench/GAIA/METR papers) — precise numbers and footnoted assumptions are something viewers should look up themselves rather than absorb from narration, and the terminology-contestedness point (Willison's essay) is better linked as further reading than compressed into voiceover.
