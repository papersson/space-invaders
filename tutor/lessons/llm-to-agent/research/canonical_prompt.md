You are a domain expert who also teaches this material. I am planning a short narrated explainer video on this lesson:

  "From LLM to agent. An LLM only writes text. Yet an AI agent reads files, runs tests and fixes a bug. How do you get from one to the other?"

Audience: non-technical to somewhat technical people. They remember ChatGPT arriving (late 2022) as "AI", and later noticed that AI started doing things, not only talking. They have not studied how any of it works.

I want the lesson to teach established, canonical knowledge, the way the standard sources (papers, well-known essays and talks, vendor and framework documentation, textbooks or course notes where they exist) teach it, not an idiosyncratic take. Report the canonical treatment. Be specific and cite the standard sources (paper and year, essay or blog post and year, documentation section, talk) for each item. Mark anything you are not sure of as uncertain instead of guessing.

1. The canonical worked example used to teach this, and why it is the standard one. If there are two competing standard examples, name both and say which is more common.
2. The standard progression used by the well-known papers, essays, talks and documentation: the order in which ideas are introduced, and which simpler version is shown before the full one.
3. The standard model, definitions and terminology: what exactly an LLM does, what exactly an agent is under the standard definitions, what the software around the model is called (and whether sources disagree on the name), and terminology that differs between sources, vendors or fields.
4. The key results, with exact figures, their assumptions, and where they stop holding. Include how reliability over many steps is usually explained.
5. The standard concrete examples (prompts with next-word probabilities, tasks, transcripts, benchmark numbers) as they appear in the canonical sources.
6. The misconceptions non-specialists typically bring about LLMs and agents, and what the canonical treatment does to correct them.
7. For a short lesson for this audience: what is essential, what is a common extra, and what should be left out.
8. Real systems and products canonically cited, with the specific mechanism each uses. In particular: how does Claude Code find the code relevant to a task in a codebase, and what have its developers said about that design choice? Cite primary sources.
9. History, with exact dates and primary sources, only as far as this question needs: when ChatGPT launched; when chat assistants first searched the web; the first widely known LLM agent attempts and how well they worked; when coding agents such as Claude Code were released; and what changed between the early attempts and agents that work, according to the people who built them.
10. Claims about this topic that are commonly overstated or subtly wrong.
11. Which parts of this topic are best learned by watching a narrated animation, which by doing (an interactive simulation, running code, an exercise), and which by reading, and why.

Answer in plain Markdown, compactly, with sources inline.

---
Run notes: both passes ran as fresh `claude -p` processes from empty scratch folders on 2026-09-27. The web pass had only WebSearch and WebFetch and was given this first line before the prompt: "Write the whole report as your reply, in Markdown. Do not create files or folders, and do not delegate: answer in this reply. Use web search and fetch the primary sources to check every date, quote and figure before you report it. Say which sources you actually read." The knowledge-only pass had no tools and was given: "Write the whole report as your reply, in Markdown. Do not create files or folders, and do not delegate: answer in this reply. Answer from what you know; you have no tools." (A first attempt without those lines answered by asking to create folders, and was rerun.)
