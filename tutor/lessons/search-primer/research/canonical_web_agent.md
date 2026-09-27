# Search Engineering & Evaluation: A Primer — Source-Checked Report

**Sources actually read this session (fetched primary text, not just search snippets):**
- Manning, Raghavan & Schütze, *Introduction to Information Retrieval* (Cambridge UP, 2008), online HTML edition, sections: "A first take at building an inverted index" (ch. 1), "TF-IDF weighting" (ch. 6.2), "Evaluation of unranked retrieval sets" (ch. 8.3), "Evaluation of ranked retrieval results" (ch. 8.4) — [nlp.stanford.edu/IR-book](https://nlp.stanford.edu/IR-book/html/htmledition/)
- Wikipedia, "Okapi BM25" (formula, defaults, variants) — [en.wikipedia.org/wiki/Okapi_BM25](https://en.wikipedia.org/wiki/Okapi_BM25)

Everything else below is cross-checked via targeted web searches against primary sources (ACM/arXiv/NIST/vendor docs); I cite each claim and flag anything not independently fetched in full text as **[unverified full text / search-snippet only]**.

---

## 1. Canonical worked examples

| Part of the pipeline | Canonical example | Source | Competing example |
|---|---|---|---|
| Inverted index construction | Shakespeare plays; Boolean query "Brutus AND Caesar AND NOT Calpurnia"; sample text from *Antony and Cleopatra* used to show tokenization → dictionary → postings lists | Manning et al., ch. 1.1, Fig. 1.4 ([nlp.stanford.edu/IR-book](https://nlp.stanford.edu/IR-book/html/htmledition/a-first-take-at-building-an-inverted-index-1.html)) | Croft/Metzler/Strohman use a small generic multi-document corpus for index construction (not independently verified this session); Büttcher/Clarke/Cormack use a similar toy-corpus approach. Manning's Shakespeare example is by far the most commonly cited/reused one in courses. |
| tf–idf weighting | The "car / auto / insurance / best" term-count table across three documents (Fig. 6.9), used to show why raw term frequency alone misranks documents and why a rare, discriminating term like "insurance" should count more than a frequent one like "car" | Manning et al., ch. 6.2, Fig. 6.9 (confirmed by fetch) | Croft et al.'s book uses its own small worked corpora for tf-idf/BM25 scoring; not independently verified here — **[unverified]**. |
| Precision/Recall | The "20 relevant documents exist; system retrieves 18 documents, 8 of them relevant" example: precision = 8/18 = 0.44, recall = 8/20 = 0.40 | Manning et al., ch. 8.3 (confirmed by fetch) | Almost every IR course reuses some version of this contingency-table example; it traces back to the Cranfield-era precision/recall formalization. |
| NDCG | The generic ranked-list-with-graded-relevance example (relevances such as 3,2,3,0,0,1,2,2,3,0) appearing in many course slides and blog explainers, tracing to Järvelin & Kekäläinen's own illustrative gain vectors | Järvelin & Kekäläinen, *ACM TOIS* 20(4), 422–446, 2002 | I could not confirm the exact "3,2,3,0,…" numbers appear in the original paper itself vs. later course slides — **[uncertain]**; treat that specific digit string as pedagogical folklore, not a verified textbook quote. |
| Whole-system relevance evaluation | Cranfield/TREC ad-hoc test collections: documents + topics + human relevance judgments | Cleverdon's Cranfield II (1,400 aerodynamics abstracts, 225 queries) and TREC ad hoc collections | These are the two competing "standard" test-collection paradigms; TREC is by far more commonly taught today because it's larger, public, and still actively used (Voorhees & Harman, *TREC: Experiment and Evaluation in Information Retrieval*, MIT Press, 2005). |

---

## 2. Standard progression (textbook order)

1. **Boolean retrieval / inverted index** first — build intuition for "how do you find documents containing a word among millions" before any ranking (Manning ch. 1–2; Croft et al. ch. 2).
2. **Text analysis / preprocessing** (tokenization, normalization, stemming, stopwords) as the step that turns raw text into index terms (Manning ch. 2; Croft et al. ch. 4).
3. **Term weighting**: raw term frequency → tf-idf → vector space model + cosine similarity (Manning ch. 6). This is always shown as a *simplification ladder*: Boolean (term present/absent) → tf only → tf-idf → cosine-normalized vectors.
4. **Probabilistic ranking / BM25** presented after vector space, as the "better, still classic, still lexical" ranking function (Manning ch. 11; Croft et al. ch. 7).
5. **Evaluation** is introduced only after a system exists to evaluate: precision/recall on unranked sets first (the simple case), then ranked evaluation (precision-recall curves, MAP, NDCG) (Manning ch. 8).
6. Modern courses then append **learning to rank → neural/dense retrieval → ANN indexing → hybrid/rerank pipelines**, mirroring the historical order: lexical (1960s–2000s) → learning-to-rank (2000s) → neural/dense (2018–present).

This progression — simple Boolean/counting model before the full probabilistic/vector model, unranked evaluation before ranked evaluation — is consistent across Manning et al. and Croft et al., and is the order used in most university IR syllabi and in TREC tutorials.

---

## 3. Standard model, definitions, notation — and where sources disagree

- **Inverted index**: *dictionary* (term → document frequency, pointer) + *postings list* (sorted document IDs, sometimes with positions/term frequency). Terminology "postings" and "dictionary" is standard across Manning, Croft, and Büttcher/Clarke/Cormack.
- **Term frequency (tf)**: count of a term in a document; **document frequency (df)**: number of documents containing the term; **inverse document frequency (idf)**: down-weights common terms.
- **Precision** = fraction of retrieved documents that are relevant = tp/(tp+fp). **Recall** = fraction of relevant documents that are retrieved = tp/(tp+fn) (Manning ch. 8.3, confirmed by fetch — exact wording quoted above).
- **F-measure**: F = 1/(α·(1/P)+(1−α)·(1/R)), with β² = (1−α)/α; balanced F1 = 2PR/(P+R) (Manning ch. 8.3, confirmed by fetch).
- **Precision@k / Recall@k**: precision/recall computed only over the top *k* results, standard in web-search-era evaluation and TREC; Manning's book discusses "precision at k" as a fixed-cutoff alternative to full precision-recall curves in ch. 8.4, motivating why MAP/NDCG were later preferred for graded, ranked evaluation.
- **MRR (Mean Reciprocal Rank)**: RR = 1/rank of the first relevant/correct item; MRR = mean of RR over queries. **Notably, this metric is *not* defined in Manning et al.'s evaluation chapter** (confirmed absent by direct fetch) — it comes from the TREC-8 Question Answering track (Voorhees, 1999) rather than the classical ad-hoc IR evaluation lineage, and is standard in Croft/Metzler/Strohman and in modern QA/passage-ranking benchmarks (e.g., MS MARCO's official metric is MRR@10). This is a genuine cross-source terminology difference worth flagging to students: MRR is canonical for tasks with (usually) one right answer; NDCG/MAP are canonical for tasks with many graded-relevant documents.
- **NDCG**: defined by Manning et al. (ch. 8.4, confirmed by fetch) using the *exponential-gain* form (below); the *original* 2002 paper used a simpler *linear-gain* form (see §4). This is the clearest documented notational divergence between "the paper that invented the metric" and "the textbook/industry form now in universal use."
- **Dense retrieval**: query and document mapped to fixed-length vectors by a neural encoder (often a "dual encoder" / "bi-encoder"); relevance ≈ vector similarity (dot product or cosine). Canonical paper: Karpukhin et al., *Dense Passage Retrieval for Open-Domain Question Answering*, EMNLP 2020 ([aclanthology.org/2020.emnlp-main.550](https://aclanthology.org/2020.emnlp-main.550/)).
- **Approximate nearest-neighbour (ANN) search**: trades exactness for speed when searching millions of vectors; canonical algorithm taught today is HNSW (Hierarchical Navigable Small World graphs), Malkov & Yashunin, *IEEE TPAMI* 42(4), 824–836, 2018, arXiv:1603.09320 (2016) — [arxiv.org/abs/1603.09320](https://arxiv.org/abs/1603.09320).
- **Hybrid search**: combining lexical (BM25) and dense retrieval result lists, typically via score/rank fusion. Canonical fusion formula: Reciprocal Rank Fusion (RRF), Cormack, Clarke & Büttcher, SIGIR 2009 — [dblp.org/rec/conf/sigir/CormackCB09](https://dblp.org/rec/conf/sigir/CormackCB09.html).
- **Reranking**: a second, more expensive model re-scores a shortlist retrieved by a fast first-stage system. Canonical paper: Nogueira & Cho, *Passage Re-ranking with BERT*, arXiv:1901.04085 (2019) — a **cross-encoder** (query+document fed jointly into BERT), as opposed to the dual/bi-encoder used for first-stage dense retrieval. This bi-encoder vs. cross-encoder distinction is the standard vocabulary split taught for "why rerankers are accurate but slow, and retrievers are fast but approximate."

---

## 4. Key formulas, as primary sources give them

**tf–idf** (Manning ch. 6.2, confirmed by fetch):
tf-idf_{t,d} = tf_{t,d} × idf_t, with score(q,d) = Σ_{t∈q} tf-idf_{t,d}. The idf term itself (ch. 6.2.1) is idf_t = log(N/df_t) (base-10 log used in the book's worked table; base doesn't matter for ranking, only for absolute scale).

**Vector space cosine similarity**: sim(d1,d2) = (V(d1)·V(d2)) / (‖V(d1)‖‖V(d2)‖) — standard across Manning ch. 6 and Croft et al.

**BM25** (Robertson & Zaragoza, *The Probabilistic Relevance Framework: BM25 and Beyond*, Foundations and Trends in IR 3(4), 2009 — [nowpublishers.com/article/Details/INR-019](https://www.nowpublishers.com/article/Details/INR-019); also Wikipedia's "Okapi BM25" page, fetched):

score(D,Q) = Σᵢ IDF(qᵢ) · [f(qᵢ,D)·(k₁+1)] / [f(qᵢ,D) + k₁·(1 − b + b·|D|/avgdl)]

- **k₁** controls term-frequency saturation, default **1.2** (commonly cited useful range 1.2–2.0).
- **b** controls length normalization, default **0.75** (b=1 full normalization, b=0 none).
- These defaults (k1=1.2, b=0.75) are the values used in TREC-era Okapi experiments and are also Lucene's/Elasticsearch's built-in defaults (Lucene `BM25Similarity` Javadoc, consistent across versions 6.0–10.3; Elastic's "Practical BM25" blog series) — [lucene.apache.org BM25Similarity](https://lucene.apache.org/core/9_9_1/core/org/apache/lucene/search/similarities/BM25Similarity.html), [elastic.co/blog/practical-bm25-part-2](https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables).
- **IDF divergence between textbook and engine form**: the classic Robertson-Sparck-Jones IDF is log[(N−n+0.5)/(n+0.5)], which can go *negative* for terms appearing in more than half the collection. Lucene/Elasticsearch (and Robertson & Zaragoza's own later presentation) instead use IDF(qᵢ) = ln[(N−n(qᵢ)+0.5)/(n(qᵢ)+0.5) + 1], adding "+1" inside the log specifically to keep the weight non-negative. This exact discrepancy across implementations is documented in Kamphuis et al., *Which BM25 Do You Mean? A Large-Scale Reproducibility Study of Scoring Variants*, ECIR 2020 — [cs.uwaterloo.ca/~jimmylin/publications/Kamphuis_etal_ECIR2020_preprint.pdf](https://cs.uwaterloo.ca/~jimmylin/publications/Kamphuis_etal_ECIR2020_preprint.pdf).

**Precision / Recall / F-measure**: as in §3, exact formulas confirmed by fetch from Manning ch. 8.3.

**11-point interpolated precision** (Manning ch. 8.4, confirmed by fetch): p_interp(r) = max_{r′≥r} p(r′), evaluated at recall levels 0.0, 0.1, …, 1.0 and averaged across queries.

**Mean Average Precision (MAP)** (Manning ch. 8.4): for each query, average the precision value computed at each rank where a relevant document is retrieved (treating un-retrieved relevant documents as contributing precision 0); MAP is the mean of this average precision over all queries.

**R-precision** (Manning ch. 8.4, confirmed by fetch): precision at rank |Rel| (the number of known relevant documents for that query); at this cutoff, precision and recall are numerically equal.

**NDCG — two forms, an important divergence**:
- *Original* (Järvelin & Kekäläinen, *ACM TOIS* 20(4), 422–446, 2002): linear-gain DCG, DCGₚ = rel₁ + Σ_{i=2}^{p} rel_i / log₂(i).
- *Textbook / industry form actually in universal use today* (Manning et al. ch. 8.4, confirmed by fetch): exponential-gain, NDCG(Q,k) = (1/|Q|) Σⱼ Z_{kj} Σ_{m=1}^{k} (2^{R(j,m)}−1)/log₂(1+m), normalized by the ideal ordering's DCG (IDCG) so a perfect ranking scores 1. The exponential form (2^rel − 1) was popularized by Burges et al., *Learning to Rank using Gradient Descent*, ICML 2005 (the RankNet paper) and is now what essentially every modern IR/learning-to-rank system, textbook, and library (e.g., XGBoost/LightGBM ranking objectives) implements. **Tell students explicitly: "NDCG" in a 2020s paper or engine almost always means the exponential-gain, log₂(1+rank) form, not the metric's own 2002 original formula.**

**MRR**: RR_q = 1/rank of first relevant result for query q (0 if none); MRR = mean over queries. Introduced as the TREC-8 QA track's primary metric (Voorhees, 1999).

**Dense retrieval / DPR training objective**: dual encoders (question encoder, passage encoder) trained with in-batch negatives so cosine/dot-product similarity of question and gold passage exceeds similarity to other in-batch passages (Karpukhin et al., 2020).

**Reciprocal Rank Fusion** (Cormack, Clarke & Büttcher, SIGIR 2009): RRFscore(d) = Σ_{r ∈ rankers} 1/(k + rank_r(d)), summing over the ranked lists being fused. The constant k damps the influence of low ranks; k=60 is the commonly used default in the paper and in production systems (e.g., Elasticsearch's RRF implementation) — **[the k=60 figure is widely repeated but I did not independently re-fetch the original paper's PDF this session to confirm the exact constant; treat as likely-correct but not re-verified in full text]**.

---

## 5. Standard numeric examples (verified)

- **Precision/recall**: 20 relevant docs exist in the collection; system retrieves 18 (8 relevant, 10 nonrelevant) → precision = 8/18 ≈ 0.44, recall = 8/20 = 0.40 (Manning ch. 8.3, fetched).
- **tf-idf**: Fig. 6.9's small term-count table across documents for "car," "auto," "insurance," "best" motivating why idf matters (Manning ch. 6.2, fetched).
- **BM25 defaults**: k1=1.2, b=0.75, used in TREC-era Okapi runs and now shipped as Lucene/Elasticsearch defaults.
- **MS MARCO passage ranking** (a widely cited benchmark numeric result, not a textbook example but the standard modern numeric anchor): BM25 baseline MRR@10 ≈ 0.167 on the dev set; Nogueira & Cho's BERT cross-encoder reranker reached MRR@10 ≈ 0.356, a roughly 2x improvement — figures reported on the official MS MARCO passage ranking leaderboard and cited across papers such as *MS MARCO: Benchmarking Ranking Models in the Large-Data Regime* (Craswell et al.) — **[figures triangulated from search snippets of the leaderboard/GitHub repo, not from the primary leaderboard page itself this session — reasonably confident but flagged]**.

---

## 6. Small public test collections for teaching / laptop-scale comparison

| Collection | Size | Judgments | Notes |
|---|---|---|---|
| **Cranfield** (Cranfield II) | 1,398 aerodynamics abstracts, 225 queries | Exhaustive relevance judgments by domain experts for every query-document pair | The historical prototype; still shipped in `ir_datasets`/PyTerrier for teaching. Small enough to judge exhaustively — this is *why* it's the historical/teaching standard. |
| **CACM** | 3,204 documents | Similar small exhaustive-judgment style | Classic Glasgow/SMART-era teaching collection. |
| **NPL / Vaswani** | ~11,000 abstracts | Provided judgments | Used heavily by the Terrier/PyTerrier project for test cases due to small size — [data.terrier.org/vaswani.dataset.html](http://data.terrier.org/vaswani.dataset.html). |
| **TREC ad hoc collections** | Varies (TIPSTER-era: ~1M docs) | Pooled judgments (see below) | Too large for a laptop demo in full, but subsets are commonly used. |
| **BEIR** (18 datasets incl. TREC-COVID, NFCorpus, SciFact, FiQA, etc.) | Each component is small (thousands to tens of thousands of docs) | Reuses each dataset's own original judgments | Thakur et al., NeurIPS Datasets & Benchmarks 2021, arXiv:2104.08663 — explicitly built as a **laptop-feasible, zero-shot comparison benchmark across lexical, dense, late-interaction, and reranking systems**; this is the modern standard for exactly the lexical-vs-dense-vs-hybrid-vs-rerank comparison this lesson wants. Its headline finding — BM25 is a strong, robust baseline; rerankers/late-interaction win on average but cost more; plain dense retrieval often underperforms out-of-domain — is a canonical talking point. |
| **MS MARCO passage ranking** | 8.8M passages, ~1M queries (subsampled dev sets used in practice) | Sparse (mostly 1 relevant passage per query) crowd-sourced from Bing click/QA data | Bajaj et al., arXiv:1611.09268 (2016). Standard modern benchmark for dense retrieval / reranking papers; official metric MRR@10. |
| **TREC-COVID** | ~51,000 CORD-19 documents (round 1) | NIST-pooled expert (biomedical) judgments, multiple rounds as the pandemic literature grew | A commonly used, laptop-feasible showcase for hybrid retrieval; e.g., pipelines combining BM25/BM25F + RRF + ColBERTv2 reranking report large nDCG@10 gains over BM25 alone — **[specific published numbers such as "51% nDCG@10 improvement" and round-by-round nDCG@10 values of ~0.56–0.73 come from secondary papers/repos found via search, not independently re-verified against the NIST TREC-COVID overview paper this session — flag these figures as indicative, not certified]**. |

TREC's judgment methodology (**pooling**): the top-N (traditionally N=100) documents from each participating system's run for a topic are merged into a pool, duplicates removed, and NIST assessors judge only the pooled documents — this is the standard way large-scale IR test collections stay affordable while still being treated as ground truth (Voorhees & Harman, MIT Press 2005; supporting studies on pool depth reliability found via search).

---

## 7. Common misconceptions and how the canonical treatment corrects them

- **"Search is just keyword matching with fancy math."** Correction: the whole lexical→dense→hybrid→rerank progression exists because keyword overlap (even weighted by BM25) misses synonymy/paraphrase, which is precisely what dense embeddings target (Karpukhin et al., 2020).
- **"A search engine computes an exact best-10 by scanning everything."** Correction: at scale, both indexing (inverted index avoids scanning every document per query) and vector retrieval (ANN/HNSW avoids scanning every embedding) are built around *not* checking every candidate; ANN is explicitly approximate — recall/quality is traded for speed (Malkov & Yashunin, 2016/2018).
- **"More relevant results retrieved = better system," ignoring ranking.** Correction: this is exactly why the field moved from unranked precision/recall to rank-aware metrics (MAP, NDCG) that reward putting the *best* results first, not merely including them somewhere in a large result set (Manning ch. 8.4).
- **"Precision and recall can both be maximized together."** Correction: Cleverdon's Cranfield-era finding of an inherent precision/recall trade-off is a foundational, still-taught result.
- **"NDCG is one universally agreed formula."** Correction, per §4: the metric's 2002 defining paper and the form implemented in nearly every modern system/library differ (linear vs. exponential gain) — a genuine, citable divergence, not student confusion to be waved away.
- **"Embeddings replace the inverted index."** Correction: in production hybrid systems, the inverted index and BM25 remain the fast, robust, and often still-best-performing first-stage component (BEIR's finding that BM25 is a strong baseline); dense retrieval augments rather than strictly supersedes it.
- **"Offline metrics (NDCG, MRR, etc.) are the whole evaluation story."** Correction: teams also run **online evaluation** (A/B tests measuring real user behavior — click-through rate, dwell time, reformulation rate, session success) because offline metrics on fixed judgments can miss real-world effects (position bias, changing user intent, judge disagreement) — this offline/online distinction should get real airtime per the prompt's emphasis.

---

## 8. What's essential vs. extra vs. cut, for a 9–10 minute video

**Essential (must include):**
- Inverted index (what problem it solves, dictionary+postings, one small worked example)
- Tokenization/normalization as the step before indexing (text analysis)
- BM25 formula at a conceptual level (term frequency saturates, idf downweights common terms, length normalization) with the k1/b defaults named
- Dense retrieval with embeddings (why: vocabulary mismatch/synonymy) + one sentence on how the vectors are trained/compared
- ANN search (why exact nearest-neighbour is too slow at scale; one mental model, e.g. graph/hierarchy navigation, without deriving HNSW)
- Hybrid search (BM25 + dense fused, e.g. RRF) and reranking (cross-encoder on a shortlist) as the modern production pipeline
- Evaluation: relevance judgments + test collections, precision/recall, precision@k, MRR, NDCG (at least the concept "graded relevance, discounted by rank"), and offline vs. online evaluation — this is explicitly asked to carry "real weight."

**Common extra (include only if time remains):**
- BM25's exact IDF variant differences across engines (§4) — good for a "if you want to go deeper" aside, not core.
- MAP / R-precision / 11-point interpolation — classical but largely superseded by NDCG/MRR in modern practice; mention MAP by name only.
- BM25F, learning-to-rank formal treatment, ColBERT-style late interaction — worth a name-drop, not an explanation.

**Leave out:**
- Full BM25/NDCG derivations and proofs, the probabilistic relevance framework's derivation, detailed HNSW graph construction algorithm, statistical significance testing of IR experiments, cross-textbook notational disputes (useful for you as the scriptwriter, not for viewers).

---

## 9. Real systems canonically cited, with mechanism

- **Google** — PageRank (link-based authority) + text-matching signals, originally described in Brin & Page, *The Anatomy of a Large-Scale Hypertextual Web Search Engine*, Computer Networks 30, 107–117, 1998 — [infolab.stanford.edu/pub/papers/google.pdf](http://infolab.stanford.edu/pub/papers/google.pdf). (Modern Google search additionally uses learned ranking and neural components, but PageRank + inverted index is the canonical historical citation for this lesson's level.)
- **Elasticsearch / Apache Lucene** — inverted index + BM25 as the default similarity/scoring function since Lucene switched from classic TF-IDF (Lucene 6, Elasticsearch 5, 2016) — Lucene `BM25Similarity` Javadoc; Elastic's "Practical BM25" series.
- **Bing** — the source of the MS MARCO dataset (real anonymized Bing query logs and passages), used as the canonical academic benchmark linking a real production system's data to public dense-retrieval/reranking research (Bajaj et al., 2016).
- **Facebook AI Research's DPR system** — canonical open-source reference implementation of dense passage retrieval, code at [github.com/facebookresearch/DPR](https://github.com/facebookresearch/DPR).
- **FAISS (Meta)** and **HNSW-based libraries** (e.g., hnswlib) — canonical ANN implementations referenced whenever HNSW/approximate nearest-neighbor is taught.

---

## 10. History, with dates and primary sources (only as far as needed)

- **1957–1966**: Cyril Cleverdon's Cranfield experiments at the College of Aeronautics, Cranfield, establish the test-collection paradigm and the terms "precision" and "recall"; Cranfield II (~1962–66) built the 1,400-document/225-query aerodynamics collection — Wikipedia "Cranfield experiments" / "Cyril Cleverdon" cross-checked via search; **exact year boundary between Cranfield I and II varies slightly across secondary sources (1961 vs. 1962/1963) — flag as a minor, non-critical date uncertainty.**
- **1975**: Salton, Wong & Yang, *A Vector Space Model for Automatic Indexing*, Communications of the ACM 18(11), 613–620 — foundational tf-idf/vector-space paper.
- **1992**: First Text REtrieval Conference (TREC), organized by NIST (Donna Harman, later Ellen Voorhees), originally to support the DARPA TIPSTER project's need for a test collection ~100x larger than any prior public collection — NIST TREC overview, ACM SIGIR Forum 33(2).
- **1994**: Robertson, Walker et al.'s Okapi system runs at TREC-3, cementing the BM25 formula and its k1=1.2/b=0.75-style defaults in practice.
- **1998**: Brin & Page publish PageRank / the Google prototype (Computer Networks 30).
- **1999**: Voorhees introduces Mean Reciprocal Rank as the primary metric for the TREC-8 QA track.
- **2002**: Järvelin & Kekäläinen publish (N)DCG, ACM TOIS 20(4).
- **2005**: Burges et al.'s RankNet paper (ICML) popularizes the exponential-gain NDCG form now in universal use.
- **2013**: Mikolov et al., word2vec, arXiv:1310.4546 (Oct 16, 2013) — the modern embeddings lineage begins.
- **2016**: Bajaj et al. release MS MARCO, arXiv:1611.09268; Malkov & Yashunin post the HNSW paper, arXiv:1603.09320.
- **2018**: Devlin et al. post BERT, arXiv:1810.04805 (published NAACL-HLT 2019) — the encoder that later powers both dense retrieval and cross-encoder reranking.
- **2019**: Nogueira & Cho, *Passage Re-ranking with BERT*, arXiv:1901.04085 — canonical cross-encoder reranking paper, tops the MS MARCO leaderboard.
- **2009**: Cormack, Clarke & Büttcher publish Reciprocal Rank Fusion at SIGIR — canonical hybrid-search fusion method (chronologically this predates the neural-era hybrid use but is the formula still cited today).
- **2020**: Karpukhin et al. publish DPR (EMNLP) — canonical modern dense-retrieval paper.
- **2021**: Thakur et al. publish BEIR (NeurIPS Datasets & Benchmarks) — canonical modern lexical-vs-dense-vs-hybrid-vs-rerank benchmark.

---

## 11. Claims commonly overstated or subtly wrong

- **"Dense retrieval / embeddings have made BM25 obsolete."** Overstated — BEIR (2021) explicitly documents BM25 as a strong, hard-to-beat zero-shot baseline; production systems retain BM25 as one leg of hybrid retrieval.
- **"NDCG is well-defined; everyone computes the same number."** Subtly wrong — the original 2002 formula and the exponential-gain form implemented almost everywhere today are different formulas (§4); reported NDCG values across tools are not always comparable without knowing which gain function and log base/discount were used.
- **"BM25 is *the* formula, unambiguous."** Subtly wrong — Kamphuis et al. (ECIR 2020) show major open-source systems ("Which BM25 do you mean?") implement meaningfully different scoring variants (e.g., the "+1" inside the IDF log) under the same name.
- **"ANN search is approximate the way BM25/tf-idf are approximate (i.e., a modeling simplification)."** Subtly wrong — ANN's approximation is about *search/retrieval completeness* (might miss the true nearest neighbor) independent of whether the underlying similarity model (the embedding) is good; conflating these two notions of "approximate" is a common student error.
- **"A/B testing (online evaluation) is strictly better than offline evaluation, so offline metrics are just a proxy to be discarded once you can A/B test."** Overstated — canonical practice keeps both: offline test collections are cheap, reproducible, and diagnostic (which component regressed?), while online tests measure real business/user impact but are slow, risky, and confounded; the standard view is that they're complementary, not that one replaces the other.
- **"Relevance judgments are objective ground truth."** Overstated — TREC's own pooling methodology is a documented, deliberate practical compromise (judging only pooled top-N documents, not the full collection), and judge disagreement/incompleteness is an actively studied limitation, not an edge case.

---

## 12. Best learned by animation vs. doing vs. reading

- **Best as narrated animation** (visual, sequential mental models, exactly your video's format): building an inverted index from documents → dictionary → postings lists; the BM25 saturation curve (why repeating a term stops helping); the "vocabulary mismatch" motivation for embeddings (two sentences meaning the same thing but sharing no words); the idea of ANN graph-hopping instead of exhaustive scan; the ranked-list-with-relevance-grades → DCG discounting → NDCG normalization pipeline; the offline-test-collection vs. online-A/B-test loop as a diagram of the engineering feedback cycle.
- **Best learned by doing** (leave for a follow-up exercise, not the video itself): computing BM25 or precision/recall/NDCG by hand on a tiny example; running BM25 vs. a dense retriever vs. a hybrid+rerank pipeline on one of the small collections in §6 (Cranfield, BEIR's TREC-COVID/SciFact, or MS MARCO dev subset) and comparing NDCG@10/MRR@10 numbers directly — this is genuinely where the "why does hybrid + rerank win" claim becomes convincing rather than asserted.
- **Best learned by reading** (reference material, not narration): the exact formula variants and default-parameter tables (§4), the primary papers (BM25, DPR, HNSW, BEIR, NDCG) for students who want to go deeper, and the TREC pooling methodology details — these are precise, notation-heavy, and better absorbed at the reader's own pace with the formula visible than spoken aloud.

---

**Summary of confidence:** Formulas and definitions directly fetched from Manning et al.'s book and Wikipedia's BM25 page are quoted verbatim/near-verbatim and high-confidence. Historical dates, other papers' formulas, and numeric benchmark results were cross-checked via targeted searches against primary-source pages (arXiv, ACM, NIST, vendor docs) but not all fetched in full text — items explicitly marked **[unverified]** or **[uncertain]** above (RRF's k=60 default, exact Cranfield I/II year boundary, specific TREC-COVID nDCG@10 numbers from secondary repos, and the "3,2,3,0,…" NDCG teaching example) should be treated as reasonably likely but not fully certified.
