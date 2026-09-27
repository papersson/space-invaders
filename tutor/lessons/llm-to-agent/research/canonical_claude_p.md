# From LLM to Agent — Canonical Content Report

## 1. Canonical worked example

Two examples compete, and they serve different purposes:

- **ReAct (Reason+Act) loop** — Yao et al., *"ReAct: Synergizing Reasoning and Acting in Language Models"* (arXiv Oct 2022, ICLR 2023). Uses a Thought → Action → Observation transcript on HotpotQA (question answering with a search-engine tool) and ALFWorld (simulated household tasks). This is the standard **conceptual** example in NLP/ML courses and papers because it's the first clean, reproducible demonstration that interleaving reasoning traces with tool calls beats either alone.
- **SWE-bench**: "reads files, runs tests, fixes a bug" (Jimenez et al., *"SWE-bench: Can Language Models Resolve Real-World GitHub Issues?"*, arXiv Oct 2023, ICLR 2024) is the standard **coding-agent** example, and it matches your lesson's phrasing almost exactly: it takes real GitHub issues + PRs, gives a model repo access, and scores whether its patch makes the associated tests pass.

For a lesson specifically about coding agents, **SWE-bench is the more common canonical example**; ReAct is the more common example when teaching the general "agent loop" concept first. Most coding-agent talks/docs (Anthropic, Cognition/Devin, OpenAI) now cite SWE-bench or its "Verified" subset as the benchmark of record.

## 2. Standard progression

The near-universal order across courses, vendor docs, and talks:

1. **LLM as next-token predictor** — Vaswani et al., *"Attention Is All You Need"* (2017, the Transformer); Radford et al., GPT-2 (2019); Brown et al., GPT-3, *"Language Models are Few-Shot Learners"* (2020).
2. **Prompting / few-shot** — Brown et al. (2020) again; in-context learning with no weight updates.
3. **Chain-of-thought prompting** — Wei et al., *"Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"* (2022) — the model reasons in text before answering, still no tools.
4. **Tool use / function calling** — Schick et al., *"Toolformer"* (Meta AI, Feb 2023); OpenAI *Function calling* docs (June 2023); Anthropic *Tool use* docs.
5. **Reasoning + acting in a loop** — ReAct (Yao et al., 2022).
6. **Autonomous multi-step agents** — AutoGPT/BabyAGI (2023, informal, not peer-reviewed) show the loop run without a human in between steps.
7. **Coding agents on real repos** — SWE-bench (2023) as the evaluation, then Devin (2024) and Claude Code (2025) as products.

Anthropic's own engineering post, *"Building Effective Agents"* (Erik Schluntz & Barry Zhang, Anthropic, Dec 19, 2024), explicitly recommends teaching in this order: start from a single LLM call, then augmented LLM (retrieval + tools + memory), then fixed multi-step **workflows**, and only then fully autonomous **agents** — arguing you should stop at the simplest structure that works. This post is widely treated as the canonical vendor-side pedagogical reference for this exact progression.

## 3. Standard definitions and terminology

- **LLM**: a model trained to predict the next token in a sequence given prior tokens (autoregressive language modeling), scaled up with the Transformer architecture (Vaswani et al., 2017; GPT series). It has no built-in ability to act on anything outside the text it emits.
- **Agent** (classic AI definition, predates LLMs): Russell & Norvig, *Artificial Intelligence: A Modern Approach* — "anything that can be viewed as perceiving its environment through sensors and acting upon that environment through actuators." This is the textbook definition most courses anchor to before specializing to LLMs.
- **LLM agent** (specialization): an LLM plus (a) a set of callable tools/actions, (b) an execution loop that runs the model repeatedly, feeding back the results of its actions ("observations"), and (c) some stopping/termination condition. This is essentially the definition used by Anthropic's "Building Effective Agents" and by LangChain's *Agents* documentation.
- **Name for the surrounding software**: sources disagree.
  - Anthropic and practitioner talk (including Claude Code discussions) often say **"harness"** or **"scaffold."**
  - LangChain calls itself an **"agent framework"**; the loop is an **"AgentExecutor."**
  - OpenAI's docs call the tool-calling mechanism **"function calling"**; Anthropic's equivalent docs call it **"tool use."** Functionally identical, named differently — worth flagging explicitly as vendor terminology drift.
  - Andrew Ng's essay/talk series (2024, *"Agentic Design Patterns"*, DeepLearning.AI *The Batch*) distinguishes **"agentic workflows"** (a broader, softer term for systems where an LLM has *any* multi-step, self-directed structure) from strict "agents," and this looser usage is common in industry talks but not in the ReAct/AIMA lineage.
- **Workflow vs. agent** (important terminology split): Anthropic's Dec 2024 post defines *workflows* as systems where LLM calls and tools are orchestrated through **predefined code paths**, and *agents* as systems where the **LLM dynamically directs its own process and tool use**, retaining control over how it accomplishes a task. This distinction is becoming the standard one cited in 2025 vendor docs.

## 4. Key results, figures, and their limits

- **SWE-bench (original, 2023)**: best models (e.g., Claude 2 with BM25 retrieval, GPT-4) resolved roughly **1–5%** of issues (figures vary by exact model/setting reported in the paper; treat single-digit low percentages as the takeaway, exact decimal uncertain to me). This established that *"read a real repo and fix a real bug"* was extremely hard for 2023-era models even with tools.
- **SWE-bench Verified** (OpenAI + original authors, blog post *"Introducing SWE-bench Verified,"* Aug 13, 2024): a human-filtered 500-issue subset removing ambiguous/unsolvable tasks, introduced because the raw benchmark had noisy, sometimes-impossible issues.
- **Claude 3.5 Sonnet (new)** — Anthropic announcement (Oct 22, 2024): **49%** on SWE-bench Verified.
- **Claude 3.7 Sonnet** — Anthropic announcement (Feb 24, 2025): reported roughly **62–70%** on SWE-bench Verified depending on scaffold/compute setting (I recall two numbers, a base score and a higher one with extended/parallel test-time compute; treat exact digits as uncertain, verify against Anthropic's model card before quoting precisely).
- **Assumptions behind all these numbers**: the model gets repo access, a defined tool set (read/edit/bash/test-runner), and often multiple attempts or extended "thinking" budgets; scores are **not** zero-shot single-generation numbers in the way classic NLP benchmarks are. Comparisons across papers only hold if the harness (tools, retries, timeout) is held constant — this is a frequently made caveat in benchmark reporting.
- **Reliability over many steps**: the standard explanatory device (used informally in many talks and posts, not one single canonical paper) is compounding per-step error: if each step succeeds independently with probability *p*, an *n*-step task succeeds with probability ≈ *pⁿ*. E.g. 95% per-step reliability over 10 steps ≈ 60% task success. This is commonly invoked to explain why agentic tasks degrade sharply with task length even when single-step accuracy looks high. **Uncertain**: I cannot point to one specific canonical paper that originates this exact framing; it appears repeatedly in practitioner talks (e.g., discussions around Karpathy's 2023 "State of GPT"-style talks) rather than in a single peer-reviewed source — flag this as a widely used heuristic, not a proven law (steps are not actually independent; agents can self-correct, which breaks the naive multiplication model).

## 5. Standard concrete examples as they appear in canonical sources

- **Next-token example**: "The cat sat on the ___" → high probability for "mat." This exact style of example is used in explainer literature such as Jay Alammar's *"The Illustrated GPT-2"* (2019) and is echoed in many textbook/course treatments of autoregressive LMs, though it is illustrative rather than from a single canonical paper.
- **ReAct transcript** (Yao et al., 2022): shows a HotpotQA question, then alternating `Thought: ...`, `Action: Search[...]`, `Observation: ...` lines, ending in `Action: Finish[answer]`. This exact transcript format is reused in many subsequent agent papers and blog posts as the template for "showing the loop."
- **SWE-bench task format**: GitHub issue text + repo snapshot as input; model outputs a diff/patch; scored by running the repo's hidden test suite (`FAIL_TO_PASS` / `PASS_TO_PASS` test sets, per the paper's terminology).
- **Devin demo** (Cognition Labs blog, March 12, 2024): narrated video of the agent reading a repo, writing code, running it, and iterating on failing tests — widely cited as the first mainstream "watch it work" coding-agent demo, though its benchmark claims were later disputed (see §10).

## 6. Misconceptions and canonical corrections

- **"The model understands/wants things."** Canonical treatments (Russell & Norvig's agent definition; Anthropic's "Building Effective Agents") frame agency as a property of the *system* (model + loop + tools), not evidence of intent or understanding in the model itself.
- **"An agent is a different, smarter kind of model."** Correction: it is typically the *same* LLM, called repeatedly by ordinary code, with tool results appended to its context. Anthropic's post is explicit that most of the "magic" is in composing simple, well-tested pieces, not a special agent-model.
- **"Running a test / editing a file is something the model does directly."** Correction: the model only emits text (e.g., a structured tool-call token sequence); a separate, deterministic piece of software (the harness) parses that text and actually invokes the shell/file-system/test-runner, then feeds the result back in as more text.
- **"Hallucination = lying."** Standard NLP treatment: the model has no concept of truth vs. falsehood as separate from likely-token continuation; it is a statistical output, not a deliberate misstatement.
- **"More autonomy is strictly better."** Anthropic's post explicitly warns that added agentic complexity introduces latency, cost, and compounding-error risk, and recommends the simplest workflow that solves the task.

## 7. What's essential vs. extra vs. cut, for a short lesson

**Essential**
- LLM = next-token predictor, no built-in ability to act (grounds the "only writes text" framing).
- The loop: model output → parsed as an action → executed by code → result fed back as text → repeat.
- The distinction between the *model* and the *harness/scaffold* (the code around it).
- One concrete example of the loop closing (e.g., "read file → see failing test → edit → rerun → pass").

**Common extra (nice, not required)**
- ReAct's Thought/Action/Observation naming.
- Naming the workflow-vs-agent distinction explicitly.
- Benchmark numbers (SWE-bench %), useful for "this used to barely work" contrast but not needed to explain the mechanism.

**Leave out for this audience**
- Transformer internals (attention, embeddings).
- Training details (RLHF, pretraining corpora).
- Framework-specific APIs (LangChain classes, function-calling JSON schemas).
- Benchmark methodology nuances (Verified vs. full SWE-bench, FAIL_TO_PASS test sets).

## 8. Real systems and mechanisms (with Claude Code detail)

- **AutoGPT** (Toran Bruce Richards, GitHub, March 30, 2023): early autonomous-loop agent using GPT-4 with a fixed set of commands (browse, write file, execute); widely reported to get stuck in repetitive loops or drift off-task — commonly cited as the "first widely known but unreliable" attempt (documented in numerous contemporaneous tech-press writeups and retrospectives rather than a single peer-reviewed source).
- **LangChain** (docs, ongoing): defines "Agents" as LLMs choosing which of a set of tools to call and in what order, via an executor loop; a framework, not a specific agent.
- **Devin** (Cognition Labs blog, March 12, 2024): claimed to resolve 13.86% of SWE-bench (unassisted) vs. much lower baselines for prior agent scaffolds on GPT-4; the specific comparison and some of the demo footage were later disputed by outside analysts as not fully representative (see §10) — flagging this as contested, not settled.
- **Claude Code** (Anthropic): released as a research preview around Feb 24, 2025 alongside Claude 3.7 Sonnet, later reaching general availability in 2025. Per Anthropic's own documentation and its engineering blog post *"Claude Code: Best practices for agentic coding"* (Anthropic Applied AI team, April 2025):
  - Claude Code does **not** build or maintain a separate semantic/embedding-based index of the repository ahead of time.
  - Instead it uses what Anthropic calls **"agentic search"**: the model is given file-system tools (list/read files, `grep`/`glob`-style search, run shell commands) and decides at each step which command to run to locate relevant code, the same way a human engineer would explore an unfamiliar repo.
  - Anthropic's stated rationale (per the blog post and public engineer commentary) is that an index-based/RAG approach goes stale as code changes and is costly to maintain per-repo/per-language, whereas on-demand agentic search always reflects the current state of the files and generalizes across languages and project structures without any indexing step. **Uncertain**: some of the more detailed rationale I recall being discussed by Anthropic engineers in podcast/interview settings (e.g., discussing why they avoided embeddings) — I'm confident in the blog post's description of the mechanism, less certain about pinning exact quotes to a specific interview, so treat those attributions as approximate.
- **SWE-bench / SWE-bench Verified** function as the shared measuring stick across all of the above products, which is why nearly every vendor announcement (Anthropic, OpenAI, Cognition) reports a SWE-bench Verified number.

## 9. History, dated

- **ChatGPT launch**: Nov 30, 2022 (OpenAI blog post, *"Introducing ChatGPT"*).
- **Earliest LLM-web-search work**: WebGPT — Nakano et al., OpenAI, *"WebGPT: Browser-assisted question-answering with human feedback"* (arXiv Dec 2021) — predates ChatGPT and is the standard academic citation for "LLM that searches the web and cites sources."
- **First mainstream chat assistant with live web browsing**: Microsoft's **Bing Chat**, launched Feb 7, 2023, built on GPT-4 with real-time search integration (Microsoft announcement, Feb 2023). ChatGPT's own official browsing feature followed later in 2023 (beta plugins mid-2023, broader "Browse with Bing" relaunch around Sept 2023).
- **First widely known LLM agent attempts**: **AutoGPT** and **BabyAGI** (both late March 2023, GitHub projects by Toran Bruce Richards and Yohei Nakajima respectively) — went viral, but widely reported as unreliable/looping in practice; no formal benchmark scores exist for these, unlike SWE-bench-era agents.
- **ReAct paper**: Yao et al., arXiv Oct 2022 / ICLR 2023 — precedes the AutoGPT wave and is the academic basis for the "loop" pattern those tools implemented informally.
- **SWE-bench**: Jimenez et al., arXiv Oct 2023 / ICLR 2024.
- **Devin** (Cognition Labs): announced March 12, 2024, marketed as "the first AI software engineer."
- **Claude Code** (Anthropic): research preview ~Feb 24, 2025; GA later in 2025.
- **What changed, per the people building these systems**: Anthropic's Dec 2024 "Building Effective Agents" post attributes reliability gains primarily to (a) better base-model instruction-following and tool-use training (not to more elaborate frameworks), and (b) keeping the surrounding scaffold simple and composable rather than adding exotic control structures. This is presented explicitly as a lesson learned from the 2023 wave of complex agent frameworks that underperformed simpler designs.

## 10. Commonly overstated or subtly wrong claims

- **"Devin is a fully autonomous AI software engineer"** — the original 13.86% SWE-bench claim and demo framing were disputed by outside reviewers who argued the comparison conditions and some demo edits were not fully like-for-like; treat as **contested**, not settled fact.
- **"Agents have goals/intentions"** — a shorthand from the classic AI-agent definition (perceive/act) that gets over-read as psychological intent; canonical sources use "goal" as a design specification, not a mental state.
- **"Bigger context window = solved reliability"** — longer context helps but doesn't address compounding multi-step error or tool-use mistakes; conflating the two is a common overstatement.
- **"Hallucination has been fixed by agents"** — giving a model tools reduces some classes of factual error (it can look things up) but does not eliminate hallucination in reasoning or in tool-call arguments.
- **"AutoGPT proved autonomous agents work"** — it proved the *idea* was compelling and viral, not that it reliably worked; its practical success rate on real tasks was low and largely anecdotal.

## 11. Animation vs. doing vs. reading

- **Best as narrated animation**: the abstract loop itself (model → action → environment → observation → back to model) and the model-vs-harness distinction — these are structural/relational ideas that benefit from a visual diagram with motion (arrows looping), which is hard to convey in static text and doesn't require audience interaction to land.
- **Best as hands-on/interactive**: actually watching (or better, driving) a coding agent fix a real failing test in a real repo — the *feel* of iterative reliability (sometimes it needs 2–3 tries, sometimes it goes down a wrong path) is something viewers should experience or watch happen live, not just be told about, because the "it doesn't always work in one shot" reality is central to honestly explaining reliability limits.
- **Best as reading**: precise terminology and benchmark caveats (SWE-bench vs. SWE-bench Verified, "workflow" vs. "agent" definitions) — these are reference-style facts better looked up/reinforced via on-screen text or show notes than absorbed purely by ear, since exact word choices matter and viewers will want to pause on them.
