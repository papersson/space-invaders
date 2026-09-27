Reviewed the full script and cross-checked every number against the evidence table (arithmetic, log calculations, BM25/TF-IDF worked examples, precision/recall/NDCG figures, and citations all check out — the sourcing here is unusually rigorous). No item rises to a "wrong, misleading, or non-canonical in a way I'd object to as a professor" level, so this is a PASS, but I have a number of precision/attribution issues worth fixing before production.

## Findings

**SHOULD FIX — Ch. 1, Google attribution generalized**
Quote: *"But a web search engine covers hundreds of billions of pages."*
The evidence backing this is a Google-specific claim ("The Google Search index covers hundreds of billions of webpages"). Generalizing it to "a web search engine" implies this is true of search engines generally, which isn't verified — other engines' index sizes differ and aren't sourced.
Fix: *"But Google's search index alone covers hundreds of billions of pages."*

**SHOULD FIX — Ch. 1, linear extrapolation glosses over memory limits**
Quote: *"At this speed, even a billion papers like these would take over ten minutes, for one query."*
The demo scan holds the whole corpus's text in memory. A corpus 5,800× larger almost certainly wouldn't fit in "this computer's" RAM, so the comparison quietly shifts from a measured result to an idealized hypothetical without saying so.
Fix: *"At this same rate — if you could even hold a billion papers like these in memory — it would take over ten minutes, for one query."*

**SHOULD FIX — Ch. 2, "coronavirus" posting-list count is really the stem's**
Quote: *"The list for origin has 5,482 papers. The list for coronavirus has 35,095."*
35,095 is the posting list for the stemmed term "coronaviru" (which also catches "coronaviruses," "coronaviral," etc.), not a count of the literal word "coronavirus" (35,098 papers, per your own evidence). The on-screen caption discloses this concurrently, but the spoken claim states it as fact about "coronavirus" before stemming has been taught — exactly the word/term conflation Chapter 3 is built to correct.
Fix: *"The list for the stored form of coronavirus has 35,095"* (or add a forward pointer: *"— we'll see in a moment why it's stored that way"*).

**SHOULD FIX — Glossary, BM25 framed as derived from TF-IDF**
Quote: *"BM25 · TF-IDF with saturation (k1) and length normalization (b)"*
BM25 doesn't historically derive from TF-IDF — it comes from the Probabilistic Relevance Framework (Robertson & Sparck Jones), independent of the vector-space TF-IDF tradition. It only functionally resembles a saturating, length-normalized TF-IDF, which is worth keeping as a teaching device, but the glossary states it as lineage.
Fix: *"BM25 · behaves like TF-IDF with saturation (k1) and length normalization (b) added, though it comes from a different theoretical framework."*

**SHOULD FIX — Ch. 6, reranker/learning-to-rank conflation**
Quote: *"Rerankers can also learn to weigh other signals, like freshness and past clicks: that's learning to rank."*
This is stated right after defining "the reranker" as the cross-encoder. But a cross-encoder takes a (query, paper) text pair as input — it doesn't ingest tabular features like freshness or click counts. Learning-to-rank models that combine such signals (e.g., LambdaMART) are typically separate models, with a text-relevance score as just one input feature among many.
Fix: *"A separate model can learn to combine this relevance score with other signals, like freshness and past clicks — that's learning to rank."*

**SHOULD FIX — Ch. 10, "the standard setup" overstates one benchmark's convention**
Quote: *"here each topic's full question is the query, the standard setup for this collection."*
This is BEIR's convention for repackaging TREC-COVID, not the original TREC evaluation's primary query field (the short "query" field used earlier, e.g. "coronavirus origin," shown as topic 1's own TREC-defined field in Chapter 7). Calling it "the standard setup for this collection" without qualification overstates its canonicity — other work on this collection uses the short query.
Fix: *"here each topic's full question is the query, following the BEIR benchmark's convention for this collection."*

**NIT — Ch. 7, judge qualifications**
Quote: *"Then people with medical expertise judged each pooled paper"*
The judges were specifically medical students (trainees) plus professional NLM indexers, not domain experts per se. Minor overstatement of qualification level.
Fix: *"medical students and professional medical librarians judged each pooled paper."*

**NIT — Ch. 7, rounding**
Quote: *"Judging every paper for each of fifty topics would take eight and a half million judgments."*
171,332 × 50 = 8,566,600, which is closer to "eight point six million" than "eight and a half million."
Fix: *"about eight point six million judgments."*

**NIT — Ch. 9/10, MRR characterization not tied back**
Ch. 9 says MRR *"suits searches with one right answer,"* then Ch. 10 applies it to TREC-COVID, which averages ~494 relevant papers per topic — not a one-right-answer task — and notes MRR barely moves as a result. The two points are consistent but the connection is left implicit.
Fix: in Ch. 10, tie it back explicitly, e.g., *"as you'd expect from a metric built for one right answer, applied to a collection where almost every topic has hundreds."*

VERDICT: PASS
