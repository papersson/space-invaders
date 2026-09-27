You are a domain expert who also teaches this material. I am planning a narrated explainer video, about nine to ten minutes long, on this lesson:

  "A primer on search engineering (information retrieval). You type a few words, and out of millions of documents a search engine returns the ten best in a fraction of a second. How does it do that? And how do the people who build it know whether a change made search better?"

Audience: relatively technical people new to the field, like an undergraduate taking a first information retrieval course. They can read a formula and a bit of code, but know nothing about search internals.

The requester wants the field's real terms, each explained, including at least: inverted index, text analysis, BM25, dense retrieval with embeddings, approximate nearest-neighbour search, hybrid search, reranking, and, with real weight, evaluation: relevance judgments, test collections, precision and recall, precision@k, recall@k, MRR, NDCG, and offline versus online evaluation.

I want the lesson to teach established, canonical knowledge, the way the standard sources (textbooks such as Manning, Raghavan and Schütze's "Introduction to Information Retrieval", Croft, Metzler and Strohman's "Search Engines: Information Retrieval in Practice", Büttcher, Clarke and Cormack's "Information Retrieval: Implementing and Evaluating Search Engines"; the original papers; TREC overview papers; and the documentation of widely used engines) teach it, not an idiosyncratic take. Report the canonical treatment. Be specific and cite the standard sources (book, chapter or section; paper and year; documentation page) for each item. Mark anything you are not sure of as uncertain instead of guessing.

1. The canonical worked examples used to teach each part of this (the index, ranking, evaluation), and why they are the standard ones. If there are competing standard examples, name them and say which is more common.
2. The standard progression the textbooks and courses use: the order in which ideas are introduced, and which simpler version is shown before the full one.
3. The standard model, definitions, notation and terminology for each part, including what exactly each evaluation metric measures, and notation or definitions that differ between textbooks, papers, engines and evaluation tools.
4. The key formulas, exactly as the primary sources give them, with their assumptions and default parameter values, and where the textbook form and the form used in widely used engines differ. Include the ranking functions and every evaluation metric named above.
5. The standard numeric examples from textbooks and papers (collection statistics, worked scoring examples, worked metric computations).
6. Small public test collections with relevance judgments that are standard for teaching, or for comparing lexical, dense, hybrid and reranked retrieval on an ordinary laptop, with how their relevance judgments were made and published results on them. Mark which numbers you are unsure of.
7. The misconceptions students typically bring to this topic, and how the canonical treatment corrects them.
8. For a lesson of this length and audience: what is essential, what is a common extra, and what should be left out.
9. Real systems canonically cited, with the mechanism each uses.
10. History, with exact dates and primary sources, only as far as this lesson needs.
11. Claims about this topic that are commonly overstated or subtly wrong.
12. Which parts of this topic are best learned by watching a narrated animation, which by doing (an interactive simulation, running code, an exercise), and which by reading, and why.

Answer in plain Markdown, compactly, with sources inline.

---
Run notes: both passes ran as fresh `claude -p` processes from empty scratch folders on 2026-09-27. The web pass had only WebSearch and WebFetch and was given this first line before the prompt: "Write the whole report as your reply, in Markdown. Do not create files or folders, and do not delegate: answer in this reply. Use web search and fetch the primary sources to check every formula, default value, date, quote and figure before you report it. Say which sources you actually read." The knowledge-only pass had no tools and was given: "Write the whole report as your reply, in Markdown. Do not create files or folders, and do not delegate: answer in this reply. Answer from what you know; you have no tools." Reports: canonical_web_agent.md, canonical_claude_p.md.
