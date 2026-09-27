# Canonical treatment of "How search engines find and rank documents, and how we know if it worked"

Sources used throughout: Manning, Raghavan & Schütze, *Introduction to Information Retrieval* (Cambridge UP, 2008) — **IIR**; Croft, Metzler & Strohman, *Search Engines: Information Retrieval in Practice* (Pearson, 2010) — **CMS**; Büttcher, Clarke & Cormack, *Information Retrieval: Implementing and Evaluating Search Engines* (MIT Press, 2010) — **BCC**; plus primary papers and TREC/engine documentation cited inline. Where I'm not confident of an exact figure or attribution I say so explicitly.

---

## 1. Canonical worked examples

- **Inverted index / Boolean retrieval**: IIR Ch. 1 opens with a tiny Shakespeare-play collection and the query `Brutus AND Caesar AND NOT Calpurnia`, motivating postings-list intersection over grep. This is *the* standard opening example in IR courses.
- **Term weighting / vector space**: IIR §6.2–6.4 uses three novels — *Sense and Sensibility*, *Pride and Prejudice*, *Wuthering Heights* — with terms like *affection, jealous, gossip, wuthering*, building a term-frequency table and computing tf-idf weights and cosine similarity. This is the standard tf-idf worked example in the field; CMS uses its own small newswire-style corpus for the same purpose but the IIR "SaS/PaP/WH" example is the one most courses reuse or clone.
- **BM25 worked example**: no single universal toy example; Robertson & Zaragoza's tutorial paper (2009, below) is the standard place a full derivation-plus-numbers walkthrough is given, and it's what most course slides adapt.
- **Evaluation / relevance judgments**: the Cranfield paradigm itself (Cleverdon, 1960s, see §10) — documents + fixed queries + human relevance judgments — is the canonical worked example of *how a test collection is built*, before any metric is computed.
- **Precision/recall by rank, and NDCG**: IIR §8.4 gives a worked ranked list with relevant/non-relevant marks to compute precision, recall, and 11-point interpolated precision, and a separate graded-relevance gain vector (I recall the sequence used is something like `(3,2,3,0,0,1,2,2,3,0)`, though I'm not fully certain of the exact digits) to compute DCG/NDCG. This is the standard NDCG teaching example cited across many courses that follow IIR.

**Competing standard**: CMS's worked examples are less quoted outside courses that adopt CMS as the primary text; IIR's examples are the ones most widely reproduced in slides/blogs, making IIR the more common source of "the" canonical numbers.

---

## 2. Standard progression

Both IIR and CMS (and most university IR courses) follow essentially the same order, which the lesson should mirror:

1. **Architecture/motivation**: why brute-force string scanning fails at scale → need an index.
2. **Inverted index**: term–document matrix → postings lists (IIR Ch. 1–2; CMS Ch. 2/5).
3. **Text analysis** (tokenization, case-folding, stopwords, stemming/lemmatization) — taught *before* scoring, since the index is built on these processed tokens (IIR Ch. 2; Porter stemmer, Porter 1980).
4. **Boolean retrieval first**, as the simplified version, then **ranked retrieval** as the "full" version (IIR explicitly does Boolean in Ch. 1, ranked in Ch. 6).
5. **Term weighting**: raw tf → tf-idf → vector space cosine similarity, as the simplified precursor to probabilistic models.
6. **Probabilistic models**: Binary Independence Model → **BM25** as the refined, practical version (IIR Ch. 11; BCC gives the fuller 2-Poisson derivation).
7. **Evaluation** is introduced early/interleaved in most modern courses (you need it to say any of the above ranking methods is "better"), formally covered as its own chapter (IIR Ch. 8; CMS Ch. 8).
8. **Modern additions** (not in the 2008–2010-era textbooks, taught via papers): word embeddings → dense/bi-encoder retrieval → ANN search as the scalability trick → hybrid combination with BM25 → cross-encoder reranking as a final refinement stage. Lin, Nogueira & Yates's *Pretrained Transformers for Text Ranking: BERT and Beyond* (2021) is the closest thing to a canonical textbook covering this later part in the same rigorous style.

The simplified-before-full pattern repeats at every layer: exact match before ranked match, raw tf before tf-idf, tf-idf/cosine before BM25, exact nearest-neighbor before approximate, single-stage retrieval before retrieve-then-rerank.

---

## 3. Standard definitions, notation, and where they diverge

- **N** = number of documents, **df_t** = document frequency of term t, **tf_{t,d}** = term frequency, **avgdl** = average document length.
- **idf_t** = log(N/df_t) (IIR eq. 6.7). Diverges in practice: classic Lucene `TFIDFSimilarity` used `1 + log(numDocs/(docFreq+1))`, a smoothed variant to avoid zero/negative values — this is the textbook-vs-engine divergence pattern that recurs everywhere below.
- **BM25's IDF term**: Robertson–Sparck-Jones (RSJ) weight `log((N-n+0.5)/(n+0.5))` can go **negative** for extremely common terms. Lucene/Elasticsearch's `BM25Similarity` adds 1 inside the log to force non-negativity (Elasticsearch docs, "Okapi BM25" similarity) — an explicit, documented textbook-vs-engine difference.
- **Precision** = relevant∩retrieved / retrieved; **Recall** = relevant∩retrieved / total relevant (IIR §8.1) — these are set-based, defined *at some cutoff*, which is exactly the point students miss (see §7).
- **Precision@k / Recall@k**: same definitions but retrieved set = top k results.
- **MRR** (Mean Reciprocal Rank): mean over queries of 1/rank of the *first* relevant document. Canonically associated with TREC-8's QA track (Voorhees, 1999) rather than ad hoc retrieval, since it assumes typically one relevant answer is enough (a "known-item"/navigational framing).
- **NDCG**: this is where notation genuinely diverges between sources.
  - Järvelin & Kekäläinen's original (SIGIR 2000; full version ACM TOIS 2002): DCG_p = rel_1 + Σ_{i=2}^{p} rel_i / log₂(i) (linear gain, discount starts at rank 2).
  - The widely used alternative (popularized via Burges et al.'s 2005 RankNet/LambdaRank paper and now the de facto ML-industry default, e.g. in many `ndcg_score` implementations): DCG_p = Σ_{i=1}^{p} (2^{rel_i} − 1) / log₂(i+1) (exponential gain, uniform discount from rank 1).
  - NDCG = DCG / IDCG, where IDCG is DCG of the ideal (relevance-sorted) ranking — this part is stable across both formulations.
  - I am **not fully certain** which exact variant `trec_eval`'s `ndcg_cut` measure implements by default versus the original IIR presentation — worth flagging to students as "check the tool," a genuinely canonical caveat rather than a gap in my knowledge alone.
- **MAP**: mean over queries of Average Precision, where AP = average of precision values at each rank where a relevant document appears (IIR §8.4).
- **Offline vs. online evaluation**: offline = metrics computed against a fixed test collection with pre-existing judgments; online = live experiments (A/B tests, interleaving) measuring user behavior. Canonical distinction discussed in Kohavi, Tang & Xu, *Trustworthy Online Controlled Experiments* (2020) for the general methodology, and Joachims (KDD 2002) plus Radlinski, Kurup & Joachims (CIKM 2008) specifically for search/interleaving.

---

## 4. Key formulas, assumptions, defaults, textbook-vs-engine gaps

**BM25** (Robertson & Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond," *Foundations and Trends in IR*, 2009; also IIR §11.4.3):

```
score(D,Q) = Σ_{t∈Q} IDF(t) · f(t,D)·(k1+1) / ( f(t,D) + k1·(1 − b + b·|D|/avgdl) )
IDF(t) = log( (N − n(t) + 0.5) / (n(t) + 0.5) )
```
Defaults: **k1 = 1.2, b = 0.75** — values that trace to Robertson & Walker's Okapi TREC-3/4 experiments and are echoed as Lucene/Elasticsearch defaults (Elasticsearch docs). Assumption: term independence, and saturating (diminishing-returns) term-frequency contribution — this saturation, plus document-length normalization via `b`, is BM25's core conceptual improvement over raw tf-idf.
The **full** RSJ/BM25 formula also has a query-term-frequency saturation factor with parameter **k3** (often k3=0 or omitted entirely in engines, which is a textbook-vs-practice simplification worth naming explicitly).

**Vector space / cosine**: score(q,d) = (q⃗·d⃗)/(‖q⃗‖‖d⃗‖), with tf-idf weighting schemes given SMART notation in IIR §6.4 (e.g. "lnc.ltc"). Pivoted length normalization (Singhal, Buckley & Mitra, SIGIR 1996) is the historical bridge between plain cosine and BM25's length-normalization term.

**Query-likelihood language model** (Ponte & Croft, SIGIR 1998): score(q,d) = P(q|d), with Dirichlet smoothing (Zhai & Lafferty, SIGIR 2001 / ACM TOIS 2004) being the canonical smoothing choice, default prior μ often around 1000–2000 in their experiments (I'd treat exact defaults as *implementation-specific*, not a fixed canon).

**Dense retrieval** (bi-encoder, DPR: Karpukhin et al., EMNLP 2020): score(q,d) = E_Q(q) · E_D(d), a dot product (not necessarily cosine — DPR is trained with dot product, a detail students often wrongly assume is always cosine).

**ANN (HNSW)** (Malkov & Yashunin, IEEE TPAMI 2018): graph-based greedy search over hierarchical proximity graphs; no closed-form "formula" per se, but the key tunable trade-off is recall vs. latency via parameters `ef_search`/`M`.

**Cross-encoder reranker** (Nogueira & Cho, arXiv 2019, "monoBERT"): score(q,d) = BERT_classifier([CLS] q [SEP] d [SEP]) — a single joint forward pass per query-document pair, contrasted with the bi-encoder's independent-encode-then-dot-product.

**Reciprocal Rank Fusion** for hybrid combination (Cormack, Clarke & Büttcher, SIGIR 2009): RRF(d) = Σ_systems 1/(k + rank_i(d)), with **k=60** the commonly used default from that paper's experiments.

**Evaluation metrics**: formulas as in §3.

---

## 5. Standard numeric examples

- IIR §6.3–6.4: full tf, log-tf, idf, and tf-idf weight table for the three-novel example, plus a cosine-similarity computation between two of the documents.
- IIR §8.1–8.4: worked ranked list of hits/misses computing precision, recall, and interpolated precision at 11 recall levels (the standard "precision-recall curve" pedagogical example); and the NDCG gain-vector example described in §1/§3.
- BCC gives a worked derivation of BM25 from the 2-Poisson model with numeric term-frequency distributions, more detailed than IIR's treatment — useful if you want to *show the derivation* rather than just state the formula.
- I don't have a single canonical "textbook" numeric BM25 score-computation example that's as universally reproduced as the tf-idf one above; most courses construct their own from the Robertson & Zaragoza (2009) formula. Treat this as a gap you may need to fill yourself rather than a specific citation.

---

## 6. Small public test collections

| Collection | Size (approx., some uncertain) | Judgments | Notes |
|---|---|---|---|
| **Cranfield** | ~1,400 abstracts, ~225 queries | Exhaustive judgments by domain experts (aeronautics) | The founding test collection, origin of the "Cranfield paradigm" (Cleverdon, 1960s); still used pedagogically. |
| **CACM** | ~3,200 documents (uncertain exact count), ~64 queries | Relevance judged, smaller-scale | Classic small collection bundled with many teaching IR toolkits (e.g. via `ir_datasets`). |
| **CISI** | ~1,460 documents (uncertain), ~112 queries | Similar | Usually paired with CACM in course exercises comparing systems. |
| **TREC ad hoc collections** | tens of thousands to millions of docs | Pooled judgments (not exhaustive) — top-k results from many participating systems are pooled and judged, per Sparck Jones & van Rijsbergen (1975) and formalized at TREC (Voorhees & Harman, *TREC: Experiment and Evaluation in IR*, MIT Press, 2005) | Standard for "real" scale but too large for a laptop demo; used as the source of the pooling *methodology* to teach, even if not run directly. |
| **BEIR subsets — NFCorpus, SciFact, TREC-COVID** | NFCorpus ~3.6k docs; SciFact ~5.2k docs; TREC-COVID ~50k–170k docs depending on round (uncertain exact figures) | Expert/pooled judgments per original dataset creators, aggregated by BEIR | Thakur, Reimers, Rücklé, Srivastava & Gurevych, "BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of IR Models," NeurIPS 2021 Datasets & Benchmarks — **the** standard modern benchmark for comparing BM25 vs. dense vs. hybrid on a laptop, explicitly designed to be small enough for that. |
| **MS MARCO passage ranking** | ~8.8M passages, but dev-small query subset is laptop-friendly | Sparse (usually one judged passage per query) | Bajaj et al., 2016/2018 — the standard large-scale training/eval set for neural rerankers; used to train DPR and monoBERT. |

**On published numbers**: BEIR's headline, oft-cited finding is that BM25 remains a strong zero-shot baseline that frequently matches or beats dense models out-of-domain, even though dense models win when trained and evaluated in-domain (e.g. on MS MARCO itself). I recall approximate nDCG@10 figures in the 0.6–0.7 range for BM25 on TREC-COVID/SciFact in the BEIR paper, but I'm **not confident enough in the exact digits** to state them as fact — treat any specific number you put on screen as needing a check against the paper's table before publishing.

---

## 7. Misconceptions and canonical corrections

- *"Search is just keyword matching."* → Canonical correction: ranking, not just matching, is the hard problem; matching is necessary but the real engineering is in scoring and evaluation.
- *"TF-IDF and BM25 are basically the same thing."* → BM25 derives from a probabilistic relevance framework (2-Poisson model), with principled saturation and length normalization, not an ad hoc tweak of tf-idf (Robertson & Zaragoza, 2009).
- *"Precision and recall are single fixed numbers for a system."* → They are inherently cutoff- and query-dependent; hence precision@k, recall@k, and averaging over many queries (MAP) exist specifically to fix this.
- *"NDCG needs binary relevance judgments."* → It's designed for graded relevance (Järvelin & Kekäläinen, 2000/2002); binary is the degenerate case.
- *"ANN search finds the actual nearest neighbors."* → It's approximate by design, trading recall for speed (HNSW, LSH); students should learn to ask "recall at what latency?"
- *"Embeddings replace keyword search."* → Motivates hybrid search directly: dense retrieval misses rare terms, exact identifiers, and out-of-domain vocabulary, which is why BM25 remains a strong baseline (BEIR, 2021) and hybrid combination is standard practice, not a hack.
- *"Click-through rate directly measures relevance."* → Position bias means users click top results more regardless of quality (Joachims et al., SIGIR 2005); this is why interleaving and careful online-experiment design exist.
- *"A/B test win = search actually got better."* → Ignores novelty effects, statistical power, and the need for guardrail metrics (Kohavi, Tang & Xu, 2020).

---

## 8. Essential vs. extra vs. omit (for a 9–10 min video)

**Essential**: inverted index & postings; brief text-analysis mention (tokenize/stem/stopwords); BM25 formula + intuition (saturation + length normalization); embeddings/dense retrieval concept; why exact nearest-neighbor is infeasible at scale → ANN concept; hybrid retrieval concept; reranking concept (cross-encoder vs. bi-encoder trade-off); relevance judgments and test collections; precision/recall; precision@k, recall@k; MRR; NDCG; offline vs. online evaluation.

**Common extra, mention briefly if time allows**: PageRank/link signals, query expansion/spelling correction, index compression, distributed sharding.

**Leave out**: full BIM/2-Poisson derivation, full HNSW graph-construction algorithm, click-model math, exact BEIR score tables, learning-to-rank algorithm internals (RankNet/LambdaMART).

---

## 9. Real systems canonically cited

- **Lucene / Elasticsearch / OpenSearch**: BM25 as default similarity, k1=1.2, b=0.75 (Elasticsearch documentation, "Okapi BM25"); also native `dense_vector`/kNN fields and hybrid ranking APIs.
- **FAISS** (Meta): the standard open-source ANN library (Johnson, Douze & Jégou, 2017/2019, "Billion-scale similarity search with GPUs").
- **Google**: publicly stated it began using BERT to better understand queries/rerank results (Google blog, "Understanding searches better than ever before," Oct 2019) — a real-world reranking example, though internal mechanism details are proprietary; mark specifics uncertain.
- **Bing**: publicly described using large-scale embeddings ("Project Turing") for retrieval in production (Microsoft blog, Nov 2019) — cite as an industry dense-retrieval example, details similarly uncertain beyond the blog post.
- **Vespa, Pinecone, Weaviate, Milvus**: documented hybrid search (BM25 + vector, combined via linear scoring or RRF) — good "this is standard industry practice" citations via their own docs.

---

## 10. History, minimally

- **1960s**: Cranfield tests (Cleverdon) — origin of the test-collection/relevance-judgment paradigm.
- **1972**: Sparck Jones, "A statistical interpretation of term specificity..." — origin of IDF.
- **1975**: Salton, Wong & Yang, "A Vector Space Model for Automatic Indexing," CACM — vector space model.
- **1976**: Robertson & Sparck Jones, probabilistic relevance model (JASIS).
- **1992**: TREC begins (NIST-sponsored).
- **1994**: Robertson, Walker et al., "Okapi at TREC-3" — BM25 introduced (name reportedly from being roughly the 25th ranking formula variant tried in that research line; treat as folklore/uncertain provenance beyond the paper itself).
- **1998**: Ponte & Croft, language-modeling approach to IR; also Brin & Page, PageRank (WWW 1998).
- **2000/2002**: Järvelin & Kekäläinen — NDCG.
- **2013**: word2vec (Mikolov et al.) — practical dense embeddings become mainstream.
- **2018**: Malkov & Yashunin — HNSW.
- **2019**: Nogueira & Cho — BERT passage reranking.
- **2020**: Karpukhin et al. — DPR, canonical modern dense retrieval.

---

## 11. Overstated or subtly wrong claims

- "Dense retrieval always beats BM25" — overstated; BEIR shows BM25 is often competitive or better zero-shot/out-of-domain.
- "BM25 is a heuristic tweak of TF-IDF" — understates its principled probabilistic derivation.
- "Cosine similarity is the embedding metric" — many production dense retrievers (DPR) are trained and used with raw dot product, not cosine.
- "ANN search is basically exact for reasonable settings" — it's a genuine recall/latency trade-off, not a rounding error.
- "TREC judgments are exhaustive/complete" — they're built via pooling and are known to be incomplete (Zobel, SIGIR 1998, on pooling reliability).
- "An A/B test win proves relevance improved" — conflates behavioral proxy metrics with actual relevance; interleaving and guardrails exist precisely because of this gap.

---

## 12. Best learning modality per component

- **Narrated animation** (best for building visual intuition of mechanism): inverted-index construction and postings-list intersection/merging; BM25's saturation curve and length-normalization effect; embedding space as a 2D/3D projection; HNSW-style graph traversal for ANN; the retrieve→rerank pipeline as a diagram; precision/recall as a Venn diagram; NDCG's rank-discount curve.
- **Hands-on / interactive** (best for concepts that only "click" by manipulating numbers): building a tiny inverted index in a few lines of Python; computing a BM25 score by hand on a toy example; running BM25 vs. a sentence-embedding model on a BEIR subset (SciFact/NFCorpus) and comparing nDCG@10 on a laptop; computing precision@k/recall@k/NDCG from a ranked list plus qrels using a library like `pytrec_eval` or `ir_measures`; trying Reciprocal Rank Fusion by hand on two ranked lists.
- **Reading** (best for precision of definition, edge cases, and derivations that don't compress into 30 seconds of narration): the exact BM25/2-Poisson derivation; formal metric definitions and their edge cases (ties, missing judgments); TREC overview papers on pooling methodology; the interleaving/online-evaluation literature, which requires careful argument rather than a visual.

---

**Bottom line for the script**: anchor each new idea to IIR's canonical worked examples (Shakespeare Boolean query → SaS/PaP/WH tf-idf → BM25 as its refinement), treat evaluation as a first-class second half built on the Cranfield paradigm and TREC pooling, be explicit whenever the textbook formula and what Elasticsearch/Lucene actually run diverge, and reserve the derivation-heavy material (2-Poisson, HNSW internals) for a "read more" pointer rather than the narration itself.
